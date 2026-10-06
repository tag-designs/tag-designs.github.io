# Tag Designs Documentation

The documentation site for the tag designs project, published to GitHub Pages
at <https://tag-designs.github.io/>. Built with
[MkDocs](https://www.mkdocs.org/) and
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Building

```sh
python3 -m pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000, live-reloads on edit
mkdocs build --strict # writes ./site
```

That is the whole toolchain: Python and two pip packages. `--strict` turns a
bad internal link or a page missing from `nav` into a failure rather than a
warning.

Through CMake, matching the rest of the project:

```sh
cmake -S . -B build
cmake --build build --target docs        # site into build/site
```

## Layout

| Path | |
| --- | --- |
| `mkdocs.yml` | Site configuration and the full `nav` |
| `docs/` | The pages, with each page's images beside it |
| `docs/stylesheets/extra.css` | Two-column grids, floated figures, reference lists |
| `check_links.py` | Resolves every relative reference in a build against disk |
| `tikz/`, `tex-images/` | LaTeX sources for the architecture diagrams |
| `bibliography/` | Zotero exports the reference lists were generated from |
| `attachments/` | Files kept with the project but not published |

## Publishing

`.github/workflows/pages.yml` builds and deploys on every push to `main`. A
manual run from the Actions tab builds only, unless the deploy box is ticked.

## Notes

**`use_directory_urls` is `true`**, unlike the MkDocs sites in the `software`
repository. Pages are served at `/docs/architecture/hardware/` rather than as
`.html` files. The content writes relative paths like `../images/x.png` that
depend on it, and it keeps published URLs unchanged from the previous Hugo
site.

**Citations are plain text.** Inline references are author-year links into a
reference list at the foot of each citing page. There is no citation plugin;
the lists were generated once from `bibliography/Nanotag-hugo.json`, which is
kept as the upstream source. A new reference is added by hand.

**Diagrams.** `cmake --build build --target images-svg` regenerates the TikZ
diagrams, and needs `pdflatex` and `pdf2svg`. The SVGs are committed, so this
is only needed when a diagram changes.

**Two known broken links.** The licenses page points at `/lgplv3.txt` and
`/software_license`, neither of which has ever existed in this repository.
`check_links.py` reports them; the CI step is non-blocking because of it.
