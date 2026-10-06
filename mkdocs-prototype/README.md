# MkDocs prototype

A working prototype, not the migration. **All 24 pages** converted to MkDocs
Material so the output can be compared against the Hugo build.

`mkdocs build --strict` passes: 26 pages, no warnings, no Hugo shortcode left
in the output. `review_diff.py` reports **0 source words missing across all
24 pages**.

```sh
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000/
mkdocs build --strict # passes clean
```

## What is here

| File | |
| --- | --- |
| `convert.py` | Hugo -> MkDocs converter: `columns`, `class`, `figure`, `cite`, `ref`, `references` |
| `convert_all.py` | Walks the whole content tree, maps page bundles, copies assets, reports anything unconverted |
| `gen_nav.py` | Emits the `nav:` block ordered by the existing Hugo `weight:` front matter |
| `review_diff.py` | Checks every word of Hugo source prose survives into the rendered page |
| `check_links.py` | Resolves every relative image and link in the built site against disk |
| `review-report.txt`, `link-report.txt` | Those checks' output |
| `mkdocs.yml` | Near-copy of `software/host/docs/mkdocs.yml`, plus arithmatex and the extra stylesheet |
| `docs/stylesheets/extra.css` | 50 lines replacing Docsy, Bootstrap, pure.css and tachyons |
| `docs/` | All 24 converted pages with their co-located images |

Regenerate everything from the live content:

```sh
python3 convert_all.py            # non-zero if any shortcode is unconverted
python3 gen_nav.py                # paste the result into mkdocs.yml
python3 -m mkdocs build --strict
python3 review_diff.py site       # non-zero if any prose went missing
python3 check_links.py site       # non-zero if an image or link is broken
```

## What the prototype established

- `columns` converts cleanly to Material grids and collapses to one column on
  a phone, as Docsy's `col-md` did. A fenced code block works as a column.
- Citations become author-year links into a generated reference list. **No
  plugin.** The bibliography JSON is read at conversion time and then leaves
  the build entirely.
- Floated figures, captioned tables and inline math all survive.

Three things only surfaced by building and looking:

1. `<figcaption>` is not a block tag `md_in_html` recognises, so a markdown
   link inside one renders literally. The converter emits a raw `<a>` there.
2. `attr="(kays2015s)"` on a figure was a bibliography key that the Hugo
   shortcode printed raw. The converter resolves it to a real citation.
3. `Nanotag-hugo.json` has malformed author fields -- `bridge2013jfo` renders
   as "Bridge, Kelly., Contina, MacCurdy, B et al." Pre-existing, and visible
   in the Hugo site too, but easy to fix once references are text.

One content issue to fix during migration: phrases like "displayed to the
right" break when a grid collapses on a phone. Already true of the Hugo site.

## What the full pass found

Converting all 24 pages turned up four things the two-page prototype could not:

1. **`class` shortcodes nest.** `pure-g` wraps two or three `pure-u-*`
   children. A single non-greedy regex pairs an outer opener with an inner
   closer and leaves 16 of them behind. The converter now matches innermost
   first and repeats.
2. **`content/en/_index.md` and `content/en/docs/_index.md` both want to be
   `index.md`.** Flattening Hugo's `docs/` prefix silently overwrote the
   landing page. The converted tree keeps the Hugo URL structure, so
   `/docs/...` still resolves and no published link breaks.
3. **One citation is written `{{< cite "key" >}}`**, quoted, where the other
   38 are bare.
4. **Five links point into Hugo's `static/` root** from the license page.
   Three of those files were copied into `docs/` and the links made relative.
   **The other two, `/lgplv3.txt` and `/software_license`, do not exist** --
   they are already broken on the live Hugo site.

Also: `static/BitTagManual.pdf`, 80 MB, is referenced by no page and no
layout. It is orphaned, and it is most of the repository.

## The review check

A true Hugo-vs-MkDocs render diff would need a Hugo build, which needs Go,
Node and Hugo Extended. `review_diff.py` does a one-directional check
instead, and for catching damage it is the stronger one: **every word of
prose in the Hugo source must appear, in order, in the rendered MkDocs
page.** Words only in the output are expected -- citation expansions and the
generated reference lists. Words only in the source are the bug signal.

Structure (headings, images, tables, code blocks) is counted separately,
because those can be lost without losing a word.

Result: 24 pages, 0 missing words, 0 structural differences.

Four known transformations are normalised rather than reported, because each
is correct: the H1 the converter promotes from front matter (Docsy rendered
the title itself), `smarty` curly quotes (Hugo's `typographer` did the same),
ordered-list numbers (CSS-generated in HTML, never text), and `{#anchor}`
attr_list syntax (consumed into an `id`).

## `use_directory_urls: true`

**Unlike the other two MkDocs sites in this project.** It is load-bearing
here, not a preference.

The content writes relative paths against Hugo's pretty URLs -- twelve images
use `../images/x.png`, written for a page served at
`/docs/architecture/hardware/`. With `use_directory_urls: false` MkDocs
serves `hardware.html` inside `/docs/architecture/`, so `../` climbs one
level too high and every one of those images silently fails: the build is
clean and the page just has gaps.

Directory URLs also keep the published URLs identical to the Hugo site, so
nothing linking in from outside breaks.

`check_links.py` exists because of this bug. It walks the built HTML and
resolves every relative reference against the filesystem: 759 checked, 2
broken, and both of those are dead in the Hugo site too (below).

## Pre-existing content bugs

Found by converting, not caused by it. All of these are live on the Hugo
site today:

- `/lgplv3.txt` and `/software_license`, linked from the license page, do
  not exist in `static/`.
- Five cross-references were never made into links and render as literal
  bracketed text: `[custom tags]`, `[link]`, `[section]`,
  `[packages to install]`, `[BitTagv6|BitTagv5|NucleoTag]`.
- `Nanotag-hugo.json` has malformed author fields (see above).
- `static/BitTagManual.pdf`, 80 MB, is referenced by nothing.

## `#center` image fragments

Twelve images carry a `#center` URL fragment -- a hugo-book convention that
outlived two theme migrations and does nothing under Docsy either. The
converter turns it into `class="center"` and the stylesheet centres them,
rather than editing twelve pages.

## Section index pages

Four Hugo branch bundles carry front matter and no body:
`docs/_index.md`, `docs/architecture/_index.md`,
`docs/userguides/fabrication/_index.md` and `talks/_index.md`. Docsy
generated a child listing on each. MkDocs has no equivalent, so
`convert_all.py` writes the listing out -- otherwise these are blank pages.

`talks/` has been dropped from the site entirely, at your request. It is
excluded in `convert_all.py` (`SKIP`) and in `review_diff.py`, so a
regeneration will not bring it back.

## Not done here

`site_url`, the Pages workflow, and a read-through of all 24 converted pages
against their Hugo renders. See the migration plan.
