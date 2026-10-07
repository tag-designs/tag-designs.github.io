# Archive

Pages retired from the published site, kept here so their content can be
checked against whatever replaced them.

Nothing in this directory is built. It sits outside `docs/`, so MkDocs does
not see it and these files are not published.

Each page here was retired for one of two reasons.

**Superseded by the software documentation.** The tag monitor, visualizer and
command-line guides described tools that the `software` repository now
documents itself, at `https://tag-designs.github.io/software/user/`. The copies
here were written for the Hugo site and had drifted: the command-line page
still described tools as planned that have since shipped, and the monitor page
predates five of the six tag families the application now configures.

| Archived | Superseded by |
| --- | --- |
| `userguides/qtmon/` | `software/host/docs/src/apps/qtmonitor.md` |
| `userguides/btviz/` | `software/host/docs/src/apps/btdataviz.md` |
| `userguides/cli/` | `software/host/docs/src/cli/` |
| `building/software/`, `building/overview/` | the software build documentation |

The one section with no counterpart, the JSON configuration file format, was
rewritten against the current proto definitions and now lives at
`software/host/docs/src/reference/config-files.md`.

**Replaced in place.** `building/index.md` is the previous version of a page
that still exists on the site. It described a monolithic repository at
`git.iu.edu/geobrown/Nanotag-paper` that no longer exists; the current page
points at the three repositories instead.

Once the replacements have been checked, this directory can go. Its history is
in git either way.
