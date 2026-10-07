# Command-Line Tools

The library that Tag Monitor is built on also backs a set of command-line
tools. They do the same work without a graphical interface, which matters in
two places: during tag fabrication, where each board is tested and clock-set in
turn, and in data processing, where a step belongs in a script rather than in a
person's hands.

| Tool | Purpose |
| --- | --- |
| `tag-test` | Set and check the internal clock, run the self-test routines |
| `tag-info` | Report hardware and firmware revisions, state and voltage |
| `tag-cal` | Calibrate a tag |
| `tag-start`, `tag-stop` | Start and stop logging |
| `tag-reset` | Reset a tag |
| `tag-dwnld` | Download data from a stopped tag |

[Command-line reference](https://tag-designs.github.io/software/user/cli/index.html){ .md-button }

Each tool's options and output are documented in the software documentation,
along with the data-processing workflow.
