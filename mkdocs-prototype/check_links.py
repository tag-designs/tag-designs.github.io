#!/usr/bin/env python3
"""Resolve every relative img/link in the built site against the filesystem.

The converted content carries relative paths written for Hugo's pretty URLs.
Whether they resolve depends on use_directory_urls, and a wrong setting
breaks images silently -- the build is clean and the page just has gaps.
This walks the built HTML and checks each target actually exists.

Usage: check_links.py <built-site-dir>
"""
import pathlib
import re
import sys
import urllib.parse

ATTR = re.compile(r'<(?:img|a|source)\b[^>]*?\b(?:src|href)="([^"]+)"', re.I)
SKIP_PREFIX = ("http://", "https://", "mailto:", "data:", "#", "//")


def main(site_dir):
    site = pathlib.Path(site_dir).resolve()
    broken, checked = [], 0

    for page in sorted(site.rglob("*.html")):
        for raw in ATTR.findall(page.read_text(errors="replace")):
            if raw.startswith(SKIP_PREFIX):
                continue
            target = urllib.parse.unquote(raw.split("#")[0].split("?")[0])
            if not target:
                continue
            checked += 1
            if target.startswith("/"):
                resolved = site / target.lstrip("/")
            else:
                resolved = (page.parent / target).resolve()
            # A directory URL is served by its index.html.
            if resolved.is_dir():
                resolved = resolved / "index.html"
            if not resolved.exists():
                broken.append((page.relative_to(site), raw))

    for page, raw in broken:
        print(f"BROKEN  {page}  ->  {raw}")
    print(f"\n{checked} relative references checked, {len(broken)} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "site"))
