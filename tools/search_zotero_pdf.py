#!/usr/bin/env python3
"""
Full-text search across all PDFs stored in Zotero.

Usage:
    python3 tools/search_zotero_pdf.py "query terms" [--context N] [--limit N]

Returns JSON with matched PDFs: filename, matched excerpts with context.

Requirements: pdftotext (poppler-utils) must be installed.
"""

import argparse
import json
import os
import re
import subprocess
import sys

ZOTERO_STORAGE = os.path.expanduser("~/Zotero/storage")
CONTEXT_LINES = 3


def extract_text(pdf_path: str) -> str | None:
    try:
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def find_matches(text: str, query_terms: list[str], context_lines: int) -> list[str]:
    lines = text.splitlines()
    pattern = re.compile("|".join(re.escape(t) for t in query_terms), re.IGNORECASE)
    seen_ranges = set()
    excerpts = []

    for i, line in enumerate(lines):
        if pattern.search(line):
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            r = (start, end)
            if r in seen_ranges:
                continue
            seen_ranges.add(r)
            snippet = "\n".join(lines[start:end]).strip()
            # Highlight matched terms
            highlighted = pattern.sub(lambda m: f"**{m.group()}**", snippet)
            excerpts.append(highlighted)

    return excerpts


def search_pdfs(query: str, context_lines: int = CONTEXT_LINES, limit: int = 10) -> list[dict]:
    terms = query.split()
    results = []

    if not os.path.isdir(ZOTERO_STORAGE):
        return [{"error": f"Zotero storage not found at {ZOTERO_STORAGE}"}]

    for root, _, files in os.walk(ZOTERO_STORAGE):
        for fname in files:
            if not fname.lower().endswith(".pdf"):
                continue
            pdf_path = os.path.join(root, fname)
            text = extract_text(pdf_path)
            if not text:
                continue
            excerpts = find_matches(text, terms, context_lines)
            if excerpts:
                results.append({
                    "file": fname,
                    "path": pdf_path,
                    "match_count": len(excerpts),
                    "excerpts": excerpts[:5],  # max 5 excerpts per file
                })

    # Sort by number of matches descending
    results.sort(key=lambda r: r["match_count"], reverse=True)
    return results[:limit]


def main():
    parser = argparse.ArgumentParser(description="Full-text search across Zotero PDFs")
    parser.add_argument("query", help="Search query (space-separated terms are ORed)")
    parser.add_argument("--context", type=int, default=CONTEXT_LINES,
                        help=f"Lines of context around each match (default: {CONTEXT_LINES})")
    parser.add_argument("--limit", type=int, default=10,
                        help="Max number of PDFs to return (default: 10)")
    args = parser.parse_args()

    results = search_pdfs(args.query, args.context, args.limit)
    output = {
        "query": args.query,
        "pdf_count": len(results),
        "results": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
