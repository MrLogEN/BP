#!/usr/bin/env python3
"""
spellcheck.py — Spell-check .tex files using aspell.

Strips LaTeX commands/environments, detects language per paragraph
(Czech diacritics → cs, otherwise en), and reports misspelled words
with suggestions.

Usage:
    python3 tools/spellcheck.py                  # all .tex files in repo root
    python3 tools/spellcheck.py --file ch.tex    # single file
    python3 tools/spellcheck.py --section "Úvod" # section by heading

Prerequisites:
    pacman -S aspell aspell-cs aspell-en
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Czech characters used for language detection
# ---------------------------------------------------------------------------
CS_CHARS = set("áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ")

# LaTeX patterns to strip before checking
_STRIP_PATTERNS = [
    re.compile(r"\\begin\{[^}]*\}.*?\\end\{[^}]*\}", re.DOTALL),  # environments
    re.compile(r"\\[a-zA-Z]+\*?\{[^}]*\}"),                        # \cmd{arg}
    re.compile(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])*"),                  # \cmd[opt]
    re.compile(r"%.*"),                                              # line comments
    re.compile(r"\$[^$]*\$"),                                       # inline math
    re.compile(r"\$\$[^$]*\$\$"),                                   # display math
    re.compile(r"[{}]"),                                             # bare braces
]


def strip_latex(text: str) -> str:
    for pattern in _STRIP_PATTERNS:
        text = pattern.sub(" ", text)
    return text


def detect_lang(paragraph: str) -> str:
    """Return 'cs' if Czech diacritics are present, else 'en'."""
    return "cs" if any(c in CS_CHARS for c in paragraph) else "en"


def _run_aspell(words: list[str], lang: str) -> dict[str, list[str]]:
    """Low-level aspell call; return {misspelled_word: [suggestions]}."""
    input_text = "\n".join(words)
    try:
        result = subprocess.run(
            ["aspell", "-l", lang, "-a"],
            input=input_text,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        sys.exit("Error: aspell not found. Install with: pacman -S aspell aspell-cs aspell-en")

    misspelled: dict[str, list[str]] = {}
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("& "):
            parts = line.split(":", 1)
            word = parts[0].split()[1]
            suggestions = [s.strip() for s in parts[1].split(",")] if len(parts) > 1 else []
            misspelled[word] = suggestions[:5]
        elif line.startswith("# "):
            word = line.split()[1]
            misspelled[word] = []
    return misspelled


def aspell_check(words: list[str], lang: str) -> dict[str, list[str]]:
    """Run aspell on a list of words; return {misspelled: [suggestions]}.

    When checking Czech text, words that are valid in English (loanwords,
    abbreviations, technical terms) are silently excluded from results.
    """
    if not words:
        return {}
    misspelled = _run_aspell(words, lang)
    if lang == "cs" and misspelled:
        # Drop words that are correct English — they are intentional loanwords
        # or abbreviations and should not be reported as Czech errors.
        en_errors = _run_aspell(list(misspelled.keys()), "en")
        misspelled = {w: s for w, s in misspelled.items() if w in en_errors}
    return misspelled


def load_custom_wordlist(repo_root: Path) -> set[str]:
    """Load custom wordlist from tools/wordlist.txt (one word per line, # comments)."""
    wl_path = repo_root / "tools" / "wordlist.txt"
    if not wl_path.exists():
        return set()
    words = set()
    for line in wl_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            words.add(line)
    return words


def check_file(path: Path, section_filter: str | None = None, custom_words: set[str] | None = None) -> list[dict]:
    """Spell-check a single .tex file and return a list of findings."""
    if custom_words is None:
        custom_words = set()
    text = path.read_text(encoding="utf-8")

    # Optional: narrow to a section
    if section_filter:
        pattern = re.compile(
            rf"(?:\\(?:chapter|section|subsection)\*?{{[^}}]*{re.escape(section_filter)}[^}}]*}})"
            rf"(.*?)(?=\\(?:chapter|section|subsection)\*?{{|$)",
            re.DOTALL | re.IGNORECASE,
        )
        m = pattern.search(text)
        if not m:
            print(f"  Section '{section_filter}' not found in {path.name}", file=sys.stderr)
            return []
        text = m.group(1)

    lines = text.splitlines()
    findings = []

    # Group lines into paragraphs (separated by blank lines)
    paragraphs: list[tuple[int, str]] = []  # (start_line, text)
    current: list[str] = []
    start_line = 1
    for i, line in enumerate(lines, start=1):
        if line.strip() == "":
            if current:
                paragraphs.append((start_line, " ".join(current)))
                current = []
        else:
            if not current:
                start_line = i
            current.append(line)
    if current:
        paragraphs.append((start_line, " ".join(current)))

    for start_line, para_text in paragraphs:
        clean = strip_latex(para_text)
        # Extract words (letters only, min 2 chars)
        words = re.findall(r"[a-zA-ZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]{2,}", clean)
        if not words:
            continue
        lang = detect_lang(clean)
        # Skip all-caps abbreviations (e.g. IEQ, IAQ, VOC) and custom wordlist entries
        words = [
            w for w in words
            if not w.isupper() and w.lower() not in {c.lower() for c in custom_words}
        ]
        misspelled = aspell_check(words, lang)
        for word, suggestions in misspelled.items():
            findings.append(
                {
                    "file": str(path),
                    "line": start_line,
                    "lang": lang,
                    "word": word,
                    "suggestions": suggestions,
                }
            )

    return findings


def print_findings(findings: list[dict]) -> None:
    if not findings:
        print("No spelling errors found.")
        return

    current_file = None
    for f in findings:
        if f["file"] != current_file:
            current_file = f["file"]
            print(f"\n=== {current_file} ===")
        sugg = ", ".join(f["suggestions"]) if f["suggestions"] else "no suggestions"
        print(f"  Line ~{f['line']:4d}  [{f['lang']}]  '{f['word']}'  →  {sugg}")
    print(f"\nTotal: {len(findings)} issue(s)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Spell-check LaTeX thesis files.")
    parser.add_argument("--file", metavar="FILE", help="Single .tex file to check")
    parser.add_argument("--section", metavar="HEADING", help="Restrict check to a section by heading text")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    custom_words = load_custom_wordlist(repo_root)

    if args.file:
        tex_files = [Path(args.file) if Path(args.file).is_absolute() else repo_root / args.file]
    else:
        tex_files = sorted(repo_root.glob("*.tex"))

    all_findings: list[dict] = []
    for tex in tex_files:
        if not tex.exists():
            print(f"File not found: {tex}", file=sys.stderr)
            continue
        all_findings.extend(check_file(tex, section_filter=args.section, custom_words=custom_words))

    print_findings(all_findings)


if __name__ == "__main__":
    main()
