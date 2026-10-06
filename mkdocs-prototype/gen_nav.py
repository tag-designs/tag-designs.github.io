#!/usr/bin/env python3
"""Emit a MkDocs nav: block ordered by the Hugo `weight:` front matter.

Hugo ordered pages implicitly through `weight:` in every file. MkDocs makes
the order explicit in mkdocs.yml, which is the point -- but the existing
weights are the authors' intent, so read them once rather than guessing.
"""
import pathlib
import re

SRC = pathlib.Path("../docs/content/en")
FM = re.compile(r"^---\n(.*?)\n---", re.S)


def meta(md):
    m = FM.match(md.read_text())
    out = {}
    if m:
        for line in m.group(1).splitlines():
            kv = re.match(r'\s*(\w+):\s*"?([^"\n]*?)"?\s*$', line)
            if kv:
                out[kv.group(1)] = kv.group(2)
    return out


def title_of(md):
    m = meta(md)
    return m.get("linkTitle") or m.get("title") or md.parent.name.title()


def weight_of(md):
    try:
        return int(meta(md).get("weight", 999))
    except ValueError:
        return 999


def walk(directory, indent):
    lines = []
    index = directory / "_index.md"
    if not index.exists():
        index = directory / "index.md"

    children = []
    for child in sorted(directory.iterdir()):
        if child.is_dir() and any(child.glob("*.md")):
            children.append(("dir", child, weight_of(
                next(iter(list(child.glob("_index.md")) + list(child.glob("index.md"))), child)), ))
        elif child.is_file() and child.suffix == ".md" and child.name not in ("_index.md", "index.md"):
            children.append(("page", child, weight_of(child)))
    children.sort(key=lambda c: (c[2], c[1].name))

    for kind, path, _ in children:
        if kind == "page":
            rel = path.relative_to(SRC)
            lines.append(f'{indent}- {title_of(path)}: {rel}')
        else:
            idx = next(iter(list(path.glob("_index.md")) + list(path.glob("index.md"))), None)
            label = title_of(idx) if idx else path.name.title()
            sub = walk(path, indent + "  ")
            rel = idx.relative_to(SRC).with_name("index.md") if idx else None
            if not sub and rel:
                lines.append(f'{indent}- {label}: {rel}')
                continue
            lines.append(f'{indent}- {label}:')
            if rel:
                lines.append(f'{indent}  - Overview: {rel}')
            lines += sub
    return lines


root_index = SRC / "_index.md"
print("nav:")
print(f'  - {title_of(root_index)}: index.md')
for line in walk(SRC, "  "):
    print(line)
