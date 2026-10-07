# Installation

A complete tag system is built from three repositories in the
[tag-designs](https://github.com/tag-designs) organization. Which one you need
depends on what you are trying to build.

| Repository | Holds | Build instructions |
| --- | --- | --- |
| [`software`](https://github.com/tag-designs/software) | Host applications and command-line tools, tag firmware, the communication protocol definitions | [Software documentation](https://tag-designs.github.io/software/) |
| [`hardware`](https://github.com/tag-designs/hardware) | KiCad board designs, fabrication outputs, mechanical designs for cases and harness jigs | [Building Hardware](hardware/index.md) |
| [`tag-designs.github.io`](https://github.com/tag-designs/tag-designs.github.io) | This site | `pip install -r requirements.txt`, then `mkdocs serve` |

Each repository builds on its own. You do not need to clone all three to work
on one of them.

## Which do you need?

**To use tags in an experiment**, you need the host applications only — Tag
Monitor to configure and download, the visualizer to inspect results. Most
people want a release build rather than a source build; see the software
documentation.

**To build or modify firmware**, you need the `software` repository and an ARM
toolchain. The embedded build is driven by CMake alongside the host build.

**To fabricate boards**, you need the `hardware` repository, KiCad and KiBot.
Board outputs are generated from the design files rather than committed.

**To assemble finished tags** from fabricated boards, see
[Tag Assembly](../userguides/fabrication/index.md).

## Prerequisites

The toolchain list is long and differs by platform, so it is kept with the
code it builds rather than duplicated here. The software documentation carries
the current list for host tools and firmware on Linux, macOS and Windows,
including CMake, Qt, protobuf and the ARM toolchain.

[Software build documentation](https://tag-designs.github.io/software/){ .md-button }
