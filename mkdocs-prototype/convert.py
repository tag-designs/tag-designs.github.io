#!/usr/bin/env python3
"""Convert Hugo/Docsy markdown to MkDocs Material markdown.

Handles the five constructs this site actually uses:

  {{< columns >}} A <---> B {{< /columns >}}   -> a Material .grid of two divs
  {{< class "x" >}} ... {{< /class >}}         -> <div class="x" markdown>
  {{< figure src=... >}}                       -> <figure> HTML
  {{< cite key >}}                             -> [Author Year](#ref-key)
  {{< references >}}                           -> a formatted reference list

Everything else -- raw HTML, pipe tables, fenced code, inline $math$ -- is left
exactly as it is, because MkDocs Material renders all of it with md_in_html,
attr_list and arithmatex enabled.

Usage: convert.py <source.md> <dest.md> [--bib bibliography.json]
"""
import argparse
import json
import re
import sys

# --------------------------------------------------------------------------
# bibliography
# --------------------------------------------------------------------------

def load_bib(path):
    with open(path) as fh:
        return {e["id"]: e for e in json.load(fh)}


def _year(entry):
    try:
        return str(entry["issued"]["date-parts"][0][0])
    except (KeyError, IndexError, TypeError):
        return "n.d."


def _family(author):
    return author.get("family") or author.get("literal") or ""


def inline_citation(entry):
    """Author-year text, APA-ish: Smith 2016 / Smith & Jones 2016 / Smith et al. 2016."""
    authors = entry.get("author") or []
    names = [_family(a) for a in authors if _family(a)]
    if not names:
        return entry.get("title", entry["id"])[:30]
    if len(names) == 1:
        who = names[0]
    elif len(names) == 2:
        who = f"{names[0]} & {names[1]}"
    else:
        who = f"{names[0]} et al."
    return f"{who} {_year(entry)}"


def reference_entry(entry):
    """One formatted reference line."""
    authors = entry.get("author") or []
    names = [_family(a) for a in authors if _family(a)]
    if not names:
        who = ""
    elif len(names) == 1:
        who = names[0]
    elif len(names) <= 5:
        who = ", ".join(names[:-1]) + " & " + names[-1]
    else:
        who = ", ".join(names[:5]) + " et al."

    bits = []
    if who:
        bits.append(f"{who} ({_year(entry)}).")
    else:
        bits.append(f"({_year(entry)}).")

    title = entry.get("title")
    if title:
        bits.append(title.rstrip(".") + ".")

    container = entry.get("container-title")
    if container:
        vol = entry.get("volume")
        issue = entry.get("issue")
        locator = f"*{container}*"
        if vol:
            locator += f", {vol}"
            if issue:
                locator += f"({issue})"
        page = entry.get("page")
        if page:
            locator += f", {page}"
        bits.append(locator.rstrip(".") + ".")
    elif entry.get("publisher"):
        bits.append(entry["publisher"].rstrip(".") + ".")

    doi = entry.get("DOI")
    url = entry.get("URL")
    if doi:
        bits.append(f"<https://doi.org/{doi}>")
    elif url:
        bits.append(f"<{url}>")

    return " ".join(bits)


# --------------------------------------------------------------------------
# shortcodes
# --------------------------------------------------------------------------

COLUMNS = re.compile(
    r"\{\{<\s*columns\s*>\}\}(?P<body>.*?)\{\{<\s*/\s*columns\s*>\}\}", re.S)
# Innermost pair only: the body may not contain another class opener.
CLASS = re.compile(
    r"\{\{<\s*class\s+\"(?P<cls>[^\"]*)\"\s*>\}\}"
    r"(?P<body>(?:(?!\{\{<\s*class\s)(?!\{\{<\s*/\s*class\s*>\}\}).)*?)"
    r"\{\{<\s*/\s*class\s*>\}\}", re.S)
FIGURE = re.compile(r"\{\{<\s*figure(?P<args>.*?)>\}\}", re.S)
CITE = re.compile(
    r"\{\{<\s*cite\s+\"?(?P<key>[A-Za-z0-9_:.\-]+)\"?\s*>\}\}")
REFERENCES = re.compile(r"\{\{<\s*references\s*>\}\}")
REF = re.compile(r"\{\{<\s*ref\s+\"(?P<target>[^\"]*)\"\s*>\}\}")
ARG = re.compile(r"(\w+)\s*=\s*(?:\"([^\"]*)\"|(\S+))")


def convert_columns(match):
    parts = [p.strip("\n") for p in match.group("body").split("<--->")]
    cells = "\n\n".join(
        f'<div markdown>\n\n{p.strip()}\n\n</div>' for p in parts if p.strip())
    return f'<div class="grid" markdown>\n\n{cells}\n\n</div>'


def convert_class(match):
    return (f'<div class="{match.group("cls")}" markdown>\n\n'
            f'{match.group("body").strip()}\n\n</div>')


def convert_figure(match, bib=None, used=None):
    args = {k: (q or u) for k, q, u in ARG.findall(match.group("args"))}
    src = args.get("src", "")
    cls = args.get("class", "")
    width = args.get("width", "")
    title = args.get("title", "")
    attr = args.get("attr", "")
    alt = args.get("alt", title)

    style = f' style="width: {width};"' if width else ""
    classes = f' class="{cls}"' if cls else ""
    caption = title
    if attr:
        attr = attr.strip("()")
        # An attribution that is actually a bibliography key -- the Hugo
        # shortcode printed these raw, e.g. "(kays2015s)". Resolve it.
        entry = (bib or {}).get(attr)
        if entry is not None:
            if used is not None:
                used.append(attr)
            rendered = (f'<a href="#ref-{attr}">'
                        f'{inline_citation(entry)}</a>')
        else:
            rendered = f"<em>{attr}</em>"
        caption = f"{caption} &mdash; {rendered}" if caption else rendered
    cap = f"\n  <figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure{classes}{style}>\n'
            f'  <img src="{src}" alt="{alt}">{cap}\n'
            f'</figure>')


# Raw HTML blocks are not markdown-processed unless they carry a `markdown`
# attribute. Any block that ended up holding a converted citation link needs
# one, or the link renders as literal [text](#ref-key).
MD_NEEDED = re.compile(
    r"<(?P<tag>div|span|p)(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>", re.S)


def mark_html_with_markdown(text):
    def fix(match):
        if "](#ref-" not in match.group("body") or "markdown" in match.group("attrs"):
            return match.group(0)
        tag, attrs, body = match.group("tag", "attrs", "body")
        return f'<{tag}{attrs} markdown="span">{body}</{tag}>'
    return MD_NEEDED.sub(fix, text)


def convert_front_matter(text):
    """Keep title; drop Hugo-only keys."""
    if not text.startswith("---"):
        return text, None
    end = text.index("\n---", 3)
    fm, body = text[3:end], text[end + 4:]
    title = None
    for line in fm.splitlines():
        m = re.match(r'\s*title:\s*"?([^"]*)"?\s*$', line)
        if m:
            title = m.group(1).strip()
            break
    return body.lstrip("\n"), title


def convert(text, bib, used):
    text, title = convert_front_matter(text)

    def cite(match):
        key = match.group("key")
        entry = bib.get(key)
        if entry is None:
            sys.stderr.write(f"  warning: no bibliography entry for {key!r}\n")
            return f"[{key}](#ref-{key})"
        used.append(key)
        return f"[{inline_citation(entry)}](#ref-{key})"

    text = COLUMNS.sub(convert_columns, text)

    # Repeat until the innermost-first pass stops changing anything.
    for _ in range(10):
        text, n = CLASS.subn(convert_class, text)
        if not n:
            break

    text = REF.sub(lambda m: m.group("target"), text)
    text = FIGURE.sub(lambda m: convert_figure(m, bib, used), text)
    text = CITE.sub(cite, text)

    text = mark_html_with_markdown(text)

    if REFERENCES.search(text):
        seen, ordered = set(), []
        for key in used:
            if key not in seen:
                seen.add(key)
                ordered.append(key)
        ordered.sort(key=lambda k: (
            (_family((bib[k].get("author") or [{}])[0]) or "").lower(), _year(bib[k])))
        lines = []
        for key in ordered:
            lines.append(f'<span id="ref-{key}"></span>'
                         f'{reference_entry(bib[key])}\n{{: .reference }}')
        text = REFERENCES.sub("\n\n".join(lines), text)

    if title:
        text = f"# {title}\n\n{text.lstrip()}"
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("dest")
    ap.add_argument("--bib")
    args = ap.parse_args()

    bib = load_bib(args.bib) if args.bib else {}
    with open(args.source) as fh:
        text = fh.read()
    out = convert(text, bib, [])
    with open(args.dest, "w") as fh:
        fh.write(out)
    print(f"{args.source} -> {args.dest}")


if __name__ == "__main__":
    main()
