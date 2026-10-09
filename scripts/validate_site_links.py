#!/usr/bin/env python3
"""Check generated portal links/assets without touching historical standalone demos.

This is a LOCAL offline generated-site check. It does not fetch remote websites,
touch Google Drive, run scientific builds or infer scientific/A9 approvals.
"""
from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PORTAL_PREFIX = "/JP_Research-and-Development/"
PRESERVED_LEGACY = {
    "methodology-demo",
    "hydropower-data-model",
    "hydropower-data-schema",
    "hydropower-data-tables",
    "hydropower-data-graph",
    "hydropower-nepal-map",
}


class References(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for field in ("href", "src"):
            value = a.get(field)
            if value and tag in {
                "a", "link", "script", "img", "source", "iframe", "video", "audio"
            }:
                self.refs.append((tag, field, value, self.getpos()[0]))


def local_target(site: Path, page: Path, value: str) -> Path | None:
    if value.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        # Treat separately hosted/public URLs as external; never request the network.
        if parsed.scheme not in ("https", "http") or parsed.netloc.lower() != "fabingurung.github.io":
            return None
        if not parsed.path.startswith(PORTAL_PREFIX):
            return None
        link = parsed.path[len(PORTAL_PREFIX):]
        proposed = site / unquote(link)
    elif parsed.path.startswith("/"):
        if not parsed.path.startswith(PORTAL_PREFIX):
            return None
        proposed = site / unquote(parsed.path[len(PORTAL_PREFIX):])
    else:
        link = unquote(parsed.path)
        if not link:
            return None
        proposed = page.parent / link

    normalized = proposed.resolve()
    if not normalized.is_relative_to(site.resolve()):
        raise ValueError("path escapes portal root")
    if value.split("?", 1)[0].split("#", 1)[0].endswith("/") or normalized.is_dir():
        normalized /= "index.html"
    return normalized


def scan(site: Path) -> dict:
    if not site.is_dir():
        raise ValueError("site directory does not exist: " + str(site))
    pages = sorted(
        p for p in site.rglob("*.html")
        if not p.relative_to(site).parts[0] in PRESERVED_LEGACY
    )
    failures = []
    inspected = 0
    for page in pages:
        parser = References()
        parser.feed(page.read_text(encoding="utf-8"))
        for tag, kind, href, lineno in parser.refs:
            try:
                target = local_target(site, page, href)
            except ValueError as exc:
                failures.append(
                    {"page": str(page.relative_to(site)), "line": lineno, "url": href, "reason": str(exc)}
                )
                continue
            if target is None:
                continue
            inspected += 1
            if not target.is_file():
                failures.append(
                    {"page": str(page.relative_to(site)), "line": lineno,
                     "url": href, "reason": "relative link target does not exist"}
                )
    return {
        "state": "PASS" if not failures else "FAIL",
        "pages_scanned": len(pages),
        "local_links_checked": inspected,
        "historical_legacy_excluded": sorted(PRESERVED_LEGACY),
        "failed_links": failures,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--site", default="dist")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    site = Path(args.site)
    if not site.is_absolute():
        site = ROOT / site
    report = scan(site)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("R&D LINK QA:", report["state"],
              "pages=", report["pages_scanned"],
              "internal_refs=", report["local_links_checked"],
              "failures=", len(report["failed_links"]))
        for bad in report["failed_links"][:40]:
            print("-", bad["page"], "line", bad["line"], bad["url"], "->", bad["reason"])
    if report["failed_links"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
