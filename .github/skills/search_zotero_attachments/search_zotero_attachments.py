#!/usr/bin/env python3
"""Full-text search across Zotero attachments (best-effort).

This script walks ~/Zotero/storage and searches across multiple attachment types.
It is intentionally dependency-light:
- PDF extraction uses `pdftotext` if available.
- DOCX extraction is implemented in pure Python (reads document.xml from the docx ZIP).
- HTML is converted to plain text using Python stdlib (HTMLParser).
- Plain-text formats are read directly.

Usage:
  python3 tools/search_zotero_attachments.py "query terms" [--context N] [--limit N]

Returns JSON with matched files and excerpts with context.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from html.parser import HTMLParser
from shutil import which
from typing import Iterable
from xml.etree import ElementTree as ET


ZOTERO_STORAGE = os.path.expanduser("~/Zotero/storage")
DEFAULT_CONTEXT_LINES = 3
DEFAULT_LIMIT = 10
DEFAULT_MAX_BYTES = 25 * 1024 * 1024  # 25 MiB


PLAIN_TEXT_EXTS = {
    ".txt", ".md", ".csv", ".tsv", ".json", ".xml", ".yml", ".yaml", ".url", ".webloc"
}
HTML_EXTS = {".html", ".htm"}
DOCX_EXTS = {".docx"}
PDF_EXTS = {".pdf"}


@dataclass
class ExtractResult:
    text: str | None
    skipped_reason: str | None = None


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []
        self._skip_depth = 0  # for script/style

    def handle_starttag(self, tag: str, attrs):
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
        elif tag in {"p", "br", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self._parts.append("\n")

    def handle_endtag(self, tag: str):
        if tag in {"script", "style", "noscript"} and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag in {"p", "div", "li", "tr"}:
            self._parts.append("\n")

    def handle_data(self, data: str):
        if self._skip_depth > 0:
            return
        if data and not data.isspace():
            self._parts.append(data)

    def get_text(self) -> str:
        # Normalize whitespace a bit while keeping line breaks
        raw = "".join(self._parts)
        raw = re.sub(r"[ \t\f\v]+", " ", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


def _read_file_limited(path: str, max_bytes: int) -> bytes | None:
    try:
        st = os.stat(path)
        if st.st_size > max_bytes:
            return None
        with open(path, "rb") as f:
            return f.read()
    except OSError:
        return None


def extract_plain_text(path: str, max_bytes: int) -> ExtractResult:
    data = _read_file_limited(path, max_bytes)
    if data is None:
        return ExtractResult(text=None, skipped_reason=f"file too large (> {max_bytes} bytes) or unreadable")
    return ExtractResult(text=data.decode("utf-8", errors="replace"))


def extract_html(path: str, max_bytes: int) -> ExtractResult:
    data = _read_file_limited(path, max_bytes)
    if data is None:
        return ExtractResult(text=None, skipped_reason=f"file too large (> {max_bytes} bytes) or unreadable")
    parser = _HTMLTextExtractor()
    try:
        parser.feed(data.decode("utf-8", errors="replace"))
        return ExtractResult(text=parser.get_text())
    except Exception as e:
        return ExtractResult(text=None, skipped_reason=f"html parse failed: {e}")


def extract_docx(path: str, max_bytes: int) -> ExtractResult:
    try:
        st = os.stat(path)
        if st.st_size > max_bytes:
            return ExtractResult(text=None, skipped_reason=f"file too large (> {max_bytes} bytes)")
    except OSError:
        return ExtractResult(text=None, skipped_reason="unreadable")

    try:
        with zipfile.ZipFile(path) as z:
            try:
                xml_bytes = z.read("word/document.xml")
            except KeyError:
                return ExtractResult(text=None, skipped_reason="missing word/document.xml")

        # Extract all <w:t> text nodes
        root = ET.fromstring(xml_bytes)
        # WordprocessingML uses namespaces; match by local-name to avoid hardcoding ns URIs
        texts: list[str] = []
        for el in root.iter():
            if el.tag.endswith("}t") and el.text:
                texts.append(el.text)
            elif el.tag.endswith("}tab"):
                texts.append("\t")
            elif el.tag.endswith("}br") or el.tag.endswith("}cr"):
                texts.append("\n")

        text = "".join(texts)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return ExtractResult(text=text.strip())
    except (zipfile.BadZipFile, ET.ParseError) as e:
        return ExtractResult(text=None, skipped_reason=f"docx parse failed: {e}")
    except Exception as e:
        return ExtractResult(text=None, skipped_reason=f"docx extract failed: {e}")


def extract_pdf(path: str, timeout_s: int = 30) -> ExtractResult:
    if which("pdftotext") is None:
        return ExtractResult(text=None, skipped_reason="pdftotext not found")

    try:
        result = subprocess.run(
            ["pdftotext", path, "-"],
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        if result.returncode != 0:
            return ExtractResult(text=None, skipped_reason="pdftotext failed")
        return ExtractResult(text=result.stdout)
    except subprocess.TimeoutExpired:
        return ExtractResult(text=None, skipped_reason="pdftotext timeout")
    except FileNotFoundError:
        return ExtractResult(text=None, skipped_reason="pdftotext not found")


def find_matches(text: str, query_terms: list[str], context_lines: int) -> list[str]:
    lines = text.splitlines()
    pattern = re.compile("|".join(re.escape(t) for t in query_terms if t), re.IGNORECASE)
    if not pattern.pattern:
        return []

    seen_ranges: set[tuple[int, int]] = set()
    excerpts: list[str] = []

    for i, line in enumerate(lines):
        if pattern.search(line):
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            r = (start, end)
            if r in seen_ranges:
                continue
            seen_ranges.add(r)
            snippet = "\n".join(lines[start:end]).strip()
            highlighted = pattern.sub(lambda m: f"**{m.group()}**", snippet)
            excerpts.append(highlighted)

    return excerpts


def _iter_files(storage_root: str) -> Iterable[str]:
    for root, _, files in os.walk(storage_root):
        for fname in files:
            yield os.path.join(root, fname)


def _normalize_exts(exts_arg: str | None) -> set[str] | None:
    if not exts_arg:
        return None
    out: set[str] = set()
    for part in exts_arg.split(","):
        p = part.strip().lower()
        if not p:
            continue
        if not p.startswith("."):
            p = "." + p
        out.add(p)
    return out or None


def search_attachments(
    query: str,
    context_lines: int = DEFAULT_CONTEXT_LINES,
    limit: int = DEFAULT_LIMIT,
    max_bytes: int = DEFAULT_MAX_BYTES,
    extensions: set[str] | None = None,
) -> dict:
    terms = query.split()
    results: list[dict] = []
    skipped: list[dict] = []

    if not os.path.isdir(ZOTERO_STORAGE):
        return {"error": f"Zotero storage not found at {ZOTERO_STORAGE}"}

    for path in _iter_files(ZOTERO_STORAGE):
        fname = os.path.basename(path)
        ext = os.path.splitext(fname)[1].lower()

        if extensions is not None and ext not in extensions:
            continue

        extract: ExtractResult
        if ext in PDF_EXTS:
            extract = extract_pdf(path)
        elif ext in DOCX_EXTS:
            extract = extract_docx(path, max_bytes=max_bytes)
        elif ext in HTML_EXTS:
            extract = extract_html(path, max_bytes=max_bytes)
        elif ext in PLAIN_TEXT_EXTS:
            extract = extract_plain_text(path, max_bytes=max_bytes)
        else:
            # Unsupported type; keep the script fast by not trying to guess
            continue

        if not extract.text:
            skipped.append({"file": fname, "path": path, "reason": extract.skipped_reason or "unknown"})
            continue

        excerpts = find_matches(extract.text, terms, context_lines)
        if excerpts:
            results.append(
                {
                    "file": fname,
                    "path": path,
                    "type": ext.lstrip("."),
                    "match_count": len(excerpts),
                    "excerpts": excerpts[:5],
                }
            )

    results.sort(key=lambda r: r["match_count"], reverse=True)
    return {
        "query": query,
        "result_count": len(results[:limit]),
        "results": results[:limit],
        "skipped_count": len(skipped),
        "skipped": skipped[:50],  # cap; debugging aid
        "notes": {
            "storage": ZOTERO_STORAGE,
            "supported_extensions": sorted(list((extensions or (PDF_EXTS | DOCX_EXTS | HTML_EXTS | PLAIN_TEXT_EXTS)))),
            "pdf_requires": "pdftotext",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Full-text search across Zotero attachments (best-effort)")
    parser.add_argument("query", help="Search query (space-separated terms are ORed)")
    parser.add_argument(
        "--context",
        type=int,
        default=DEFAULT_CONTEXT_LINES,
        help=f"Lines of context around each match (default: {DEFAULT_CONTEXT_LINES})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Max number of matching files to return (default: {DEFAULT_LIMIT})",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=DEFAULT_MAX_BYTES,
        help=f"Skip non-PDF files larger than this size (default: {DEFAULT_MAX_BYTES})",
    )
    parser.add_argument(
        "--extensions",
        type=str,
        default=None,
        help="Comma-separated list of extensions to include (e.g. pdf,docx,html,txt). Default: all supported.",
    )
    args = parser.parse_args()

    exts = _normalize_exts(args.extensions)
    output = search_attachments(
        args.query,
        context_lines=args.context,
        limit=args.limit,
        max_bytes=args.max_bytes,
        extensions=exts,
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
