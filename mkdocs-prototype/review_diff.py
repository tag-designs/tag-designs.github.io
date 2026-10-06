#!/usr/bin/env python3
"""Check that nothing was lost converting Hugo source to MkDocs output.

A true Hugo-vs-MkDocs render diff would need a Hugo build, which this
environment cannot do. This is a one-directional check instead, and for
catching damage it is the stronger one:

    every word of prose in the Hugo SOURCE must appear, in order,
    in the RENDERED MkDocs page.

Words present only in the output are expected -- citation expansions
("Bridge et al. 2013") and the generated reference lists. Words present only
in the source are the bug signal: prose the converter dropped, or markdown
that failed to render.

Structural counts (headings, images, links, tables, code blocks) are compared
separately, because those can be lost without losing a word.

Usage: review_diff.py <built-site-dir>
"""
import difflib
import html
import pathlib
import re
import sys
from html.parser import HTMLParser

SRC = pathlib.Path("../docs/content/en")
OUT = pathlib.Path("docs")

SKIP_TAGS = {"script", "style", "nav", "header", "footer", "label", "svg"}


class Text(HTMLParser):
    """Rendered text plus structural counts, from a built page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip, self.depth = [], 0, 0
        self.inmain = False
        self.counts = dict(h=0, img=0, a=0, table=0, pre=0)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        # Material wraps the page body in <article>; everything else is chrome.
        if tag == "article":
            self.inmain, self.depth = True, 0
        if self.inmain:
            self.depth += 1
            if tag in SKIP_TAGS:
                self.skip += 1
            if tag in ("h1", "h2", "h3", "h4"):
                self.counts["h"] += 1
            elif tag == "img":
                self.counts["img"] += 1
            elif tag == "a" and not a.get("class", "").startswith("head"):
                self.counts["a"] += 1
            elif tag == "table":
                self.counts["table"] += 1
            elif tag == "pre":
                self.counts["pre"] += 1

    def handle_endtag(self, tag):
        if not self.inmain:
            return
        if tag in SKIP_TAGS and self.skip:
            self.skip -= 1
        self.depth -= 1
        if tag == "article":
            self.inmain = False

    def handle_data(self, data):
        if self.inmain and not self.skip:
            self.parts.append(data)

    def text(self):
        return " ".join(self.parts)


# A file may end immediately after its front matter, with no trailing newline.
FRONT = re.compile(r"\A---\n.*?\n---[ \t]*(?:\n|\Z)", re.S)
SHORTCODE = re.compile(r"\{\{[<%].*?[>%]\}\}", re.S)
HTMLTAG = re.compile(r"<[^>]+>")
FENCE = re.compile(r"```.*?```", re.S)
MDLINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
WORD = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")

# smarty turns ' into a curly apostrophe and -- into an en dash, exactly as
# Hugo's typographer did. Normalise both sides before comparing words.
SMART = str.maketrans({"\u2019": "'", "\u2018": "'", "\u201c": '"',
                       "\u201d": '"', "\u2013": "-", "\u2014": "-"})


def source_counts(text):
    # Count AFTER removing fences: a shell comment inside a ```text block
    # ("#  Running test") is not a heading.
    fences = len(re.findall(r"^```", text, re.M)) // 2
    text = FENCE.sub("\n", text)
    return dict(
        # +1: the converter promotes the front-matter title to an H1, which
        # Docsy rendered from front matter instead. Expected on every page.
        h=len(re.findall(r"^#{1,4} ", text, re.M)) + 1,
        img=(len(re.findall(r"<img\b", text))
             + len(re.findall(r"!\[", text))
             + len(re.findall(r"\{\{<\s*figure\b", text))),
        table=len(re.findall(r"^\|.*\|\s*$\n^\|[\s:|-]+\|\s*$", text, re.M)),
        pre=fences,
    )


def source_words(path):
    t = path.read_text()
    t = FRONT.sub("", t)
    counts = source_counts(t)
    # Ordered-list markers are CSS-generated in HTML, never text.
    t = re.sub(r"^\s*\d+[.)]\s", " ", t, flags=re.M)
    t = FENCE.sub(" ", t)          # code is compared by count, not by word
    t = SHORTCODE.sub(" ", t)      # a shortcode's own syntax is not prose
    t = t.replace("<--->", " ")
    t = HTMLTAG.sub(" ", t)
    t = re.sub(r"\{#[A-Za-z0-9_-]+\}", " ", t)
    t = MDLINK.sub(r"\1", t)
    t = html.unescape(t).translate(SMART)
    return WORD.findall(t), counts


def dest_for(md):
    parts = list(md.relative_to(SRC).parts)
    if parts[-1] in ("_index.md", "index.md"):
        parts[-1] = "index.md"
    return OUT.joinpath(*parts)


def main(site_dir):
    site = pathlib.Path(site_dir)
    total_missing, pages, problems = 0, 0, []

    for md in sorted(SRC.rglob("*.md")):
        if set(md.relative_to(SRC).parts) & {"talks"}:   # dropped from the site
            continue
        dest = dest_for(md)
        rel = dest.relative_to(OUT)
        page = (site / rel.parent / "index.html" if rel.name == "index.md"
                else site / rel.with_suffix("") / "index.html")
        if not page.exists():
            problems.append((str(dest), "NO BUILT PAGE", [], {}, {}))
            continue

        want, scount = source_words(md)
        parser = Text()
        parser.feed(page.read_text())
        got = WORD.findall(html.unescape(parser.text()).translate(SMART))
        gcount = parser.counts

        missing = [w for tag, i1, i2, _, _ in
                   difflib.SequenceMatcher(None, want, got, autojunk=False)
                   .get_opcodes() if tag in ("delete", "replace")
                   for w in want[i1:i2]]

        pages += 1
        total_missing += len(missing)
        struct = []
        for k, label in (("h", "headings"), ("img", "images"),
                         ("table", "tables"), ("pre", "code blocks")):
            if scount.get(k, 0) != gcount.get(k, 0):
                struct.append(f"{label} {scount.get(k,0)}->{gcount.get(k,0)}")

        if missing or struct:
            problems.append((str(dest), "", missing, scount, gcount))
            print(f"\n{dest}")
            print(f"  words: {len(want)} source -> {len(got)} rendered")
            if struct:
                print(f"  STRUCTURE: {'; '.join(struct)}")
            if missing:
                print(f"  MISSING {len(missing)} word(s): "
                      f"{' '.join(missing[:40])}{' ...' if len(missing) > 40 else ''}")
        else:
            print(f"OK  {dest}  ({len(want)} words)")

    print(f"\n{'='*64}")
    print(f"{pages} pages checked, {total_missing} source words missing from output")
    print(f"{len(problems)} page(s) with anything to look at")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "site"))
