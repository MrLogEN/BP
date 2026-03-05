#!/usr/bin/env python3
"""
Google Scholar fallback search tool for thesis research.

Usage:
    python3 tools/search_scholar.py "your search query" [--limit N]

Returns JSON with results: title, authors, abstract, year, url, citation_count.

Note: scholarly scrapes Google Scholar and may be blocked by CAPTCHA.
      If blocked, a warning is printed and results may be incomplete.
      SFX@VSE full-text access must be verified manually via the returned URLs.
"""

import argparse
import json
import sys

try:
    from scholarly import scholarly
except ImportError:
    print(json.dumps({"error": "scholarly not installed. Run: ~/.local/bin/pip install scholarly --user --break-system-packages"}))
    sys.exit(1)


def search(query: str, limit: int = 5) -> list[dict]:
    results = []
    try:
        search_query = scholarly.search_pubs(query)
        for _ in range(limit):
            try:
                pub = next(search_query)
                bib = pub.get("bib", {})
                results.append({
                    "title": bib.get("title", ""),
                    "authors": bib.get("author", []),
                    "abstract": bib.get("abstract", "")[:500] if bib.get("abstract") else "",
                    "year": bib.get("pub_year", ""),
                    "venue": bib.get("venue", ""),
                    "url": pub.get("pub_url") or pub.get("eprint_url") or "",
                    "citation_count": pub.get("num_citations", 0),
                })
            except StopIteration:
                break
    except Exception as e:
        err = str(e)
        if "CAPTCHA" in err or "Too Many Requests" in err or "blocked" in err.lower():
            print(json.dumps({"warning": "Google Scholar blocked the request (CAPTCHA). Try again later or use a VPN.", "results": results}))
            sys.exit(2)
        else:
            print(json.dumps({"error": err, "results": results}))
            sys.exit(1)
    return results


def main():
    parser = argparse.ArgumentParser(description="Search Google Scholar via scholarly")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Max results to return (default: 5)")
    args = parser.parse_args()

    results = search(args.query, args.limit)
    output = {
        "query": args.query,
        "count": len(results),
        "results": results,
        "note": "SFX@VSE full-text access must be verified manually. Add relevant sources to Zotero."
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
