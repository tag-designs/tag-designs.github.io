#!/usr/bin/env python3
"""Convert the whole Hugo content tree to a MkDocs docs/ tree.

Maps Hugo page bundles onto MkDocs directories:

  content/en/_index.md                      -> docs/index.md
  content/en/docs/architecture/_index.md    -> docs/architecture/index.md
  content/en/docs/architecture/hardware.md  -> docs/architecture/hardware.md
  content/en/docs/contact.md                -> docs/contact.md

Co-located image directories are copied beside their page, so the relative
src="images/x.png" links in the content keep working untouched. Site-absolute
src="/images/x.png" references are rewritten to reach docs/images/.
"""
import pathlib
import re
import shutil
import sys

import convert as C

FM = re.compile(r"\A---\n(.*?)\n---", re.S)


def front(md):
    m = FM.match(md.read_text())
    out = {}
    if m:
        for line in m.group(1).splitlines():
            kv = re.match(r'\s*(\w+):\s*>?\s*"?([^"\n]*?)"?\s*$', line)
            if kv and kv.group(2):
                out[kv.group(1)] = kv.group(2)
    return out


def section_body(md):
    """What Docsy generated for a section page: its description and a list of
    child pages. Hugo branch bundles often carry no body at all and relied on
    the theme for this; MkDocs has no equivalent, so write it out."""
    lines = []
    desc = front(md).get("description")
    if desc:
        lines.append(desc.strip('"'))

    children = []
    for child in sorted(md.parent.iterdir()):
        if child.is_dir():
            idx = next(iter(list(child.glob("_index.md"))
                            + list(child.glob("index.md"))), None)
            if idx:
                children.append((front(idx).get("linkTitle")
                                 or front(idx).get("title")
                                 or child.name, f"{child.name}/index.md"))
        elif child.suffix == ".md" and child.name not in ("_index.md", "index.md"):
            children.append((front(child).get("linkTitle")
                             or front(child).get("title")
                             or child.stem, child.name))
    if children:
        lines.append("")
        lines += [f"- [{title}]({link})" for title, link in children]
    return "\n".join(lines)

SRC = pathlib.Path("../docs/content/en")
STATIC = pathlib.Path("../docs/static")
OUT = pathlib.Path("docs")
BIB = pathlib.Path("../docs/resources/Nanotag-hugo.json")

# Hugo nests everything one level under content/en/docs; flatten that away.
def dest_for(md):
    rel = md.relative_to(SRC)
    parts = list(rel.parts)
    if parts[-1] in ("_index.md", "index.md"):
        parts[-1] = "index.md"
    return OUT.joinpath(*parts)


# Pages dropped from the site.
SKIP = {"talks"}


def depth_prefix(dest):
    """Relative path from a page's URL back up to the site root.

    With use_directory_urls, docs/a/b.md and docs/a/b/index.md are both
    served at /a/b/, so the depth is the number of URL segments, not the
    number of path components.
    """
    parts = list(dest.relative_to(OUT).parts)
    if parts[-1] == "index.md":
        parts.pop()
    else:
        parts[-1] = parts[-1][:-3]
    return "../" * len(parts)


def main():
    bib = C.load_bib(BIB)
    pages, unknown, missing_static = [], {}, set()

    for md in sorted(SRC.rglob("*.md")):
        if set(md.relative_to(SRC).parts) & SKIP:
            continue
        dest = dest_for(md)
        dest.parent.mkdir(parents=True, exist_ok=True)

        text = md.read_text()
        out = C.convert(text, bib, [])

        # A front-matter-only branch bundle rendered as a section listing
        # under Docsy. Without a body it is a blank page in MkDocs.
        if len(out.strip().splitlines()) <= 1:
            body = section_body(md)
            if body:
                out = out.rstrip() + "\n\n" + body + "\n"

        # Site-absolute references. Hugo served anything in static/ from the
        # site root; MkDocs serves docs/, so these become relative and the
        # files are copied across. A .md copied into docs/ is rendered as a
        # page, so it is linked by its directory URL, not its filename.
        prefix = depth_prefix(dest)
        out = re.sub(r'(src=["\'])/images/', rf'\1{prefix}images/', out)
        out = re.sub(r'\]\(/images/', f']({prefix}images/', out)

        for ref in sorted(set(re.findall(r'(?:src=\"|\]\()/([A-Za-z0-9._-]+)', out))):
            src_file = STATIC / ref
            if not src_file.is_file():
                missing_static.add(ref)        # already broken under Hugo
                continue
            if not (OUT / ref).exists():
                shutil.copy2(src_file, OUT / ref)
            target = (f"{prefix}{ref[:-3]}/" if ref.endswith(".md")
                      else f"{prefix}{ref}")
            out = out.replace(f'"/{ref}"', f'"{target}"').replace(
                f"](/{ref})", f"]({target})")

        out = re.sub(r'(<img\b[^>]*?)src="([^"]*?)#\s*center"',
                     r'\1class="center" src="\2"', out)

        for m in re.finditer(r"\{\{[<%]\s*/?\s*([a-zA-Z/-]+)", out):
            unknown.setdefault(m.group(1), []).append(str(dest))

        dest.write_text(out)

        # Co-located page-bundle assets: an asset directory holds no
        # markdown. A branch bundle's siblings are content, not assets.
        for sub in md.parent.iterdir():
            if not sub.is_dir() or any(sub.rglob("*.md")):
                continue
            target = dest.parent / sub.name
            if not target.exists():
                shutil.copytree(sub, target)
        pages.append((md, dest))

    # Site-wide static images referenced as /images/...
    (OUT / "images").mkdir(exist_ok=True)
    for png in (STATIC / "images").glob("*"):
        if png.is_file() and not (OUT / "images" / png.name).exists():
            shutil.copy2(png, OUT / "images" / png.name)

    for src, dest in pages:
        print(f"  {src.relative_to(SRC)} -> {dest.relative_to(OUT)}")
    print(f"\n{len(pages)} pages converted")

    if missing_static:
        print("\nLINKS TO FILES THAT DO NOT EXIST IN static/ "
              "(already broken on the Hugo site):", file=sys.stderr)
        for ref in sorted(missing_static):
            print(f"  /{ref}", file=sys.stderr)

    if unknown:
        print("\nUNCONVERTED SHORTCODES:", file=sys.stderr)
        for name, where in sorted(unknown.items()):
            print(f"  {name}: {len(where)} in {sorted(set(where))}", file=sys.stderr)
        return 1
    print("No unconverted shortcodes remain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
