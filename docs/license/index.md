# Licenses

The project's own code, host software and firmware alike, is licensed under the
[MIT License](https://github.com/tag-designs/software/blob/main/LICENSE),
Copyright &copy; 2018&ndash;2026 The Trustees of Indiana University. Some
base-firmware files carry their own notice, "Copyright 2018 Geoffrey Brown,
Licensed under the Apache License, Version 2.0", and remain under that license.

Several of the programs built from that code link components that are available
only under the GPL. Those programs, as distributed, are therefore covered by the
[GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.html):

| Distributed program | GPL component | Its license |
| --- | --- | --- |
| Every tag and base-board firmware image | ChibiOS/RT kernel, OS library and Cortex&#8209;M ports | GPL-3.0-only |
| `sensorviz`, `btviz` | QCustomPlot 2.1.1, statically linked | GPL-3.0-or-later |
| `qtcalibrate` | Qt Quick 3D and Qt Quick Timeline | GPL-3.0-only |

MIT is compatible with GPL-3.0, so the MIT code can be combined into those
programs. Each program as a whole is conveyed under GPL-3.0, while the MIT
grant still applies to the project's own code taken on its own. The remaining
host programs and the external flash loaders contain no GPL code.

## Third-party components

The software repository carries one index per side, listing every third-party
component with its version, its license, and which programs it is used in. Each
component has a notice file giving its copyright, where it is used and where its
source is. These are the authoritative lists, kept beside the code they
describe:

[Host tools and their manual](https://github.com/tag-designs/software/blob/main/LICENSES/host/README.md){ .md-button }
[Firmware and flash loaders](https://github.com/tag-designs/software/blob/main/LICENSES/embedded/README.md){ .md-button }

The same files travel with the software itself rather than only living on
GitHub: the host packages install them as `tag_tools/licenses`, builds that
install firmware or loaders place them alongside as `licenses/`, and the
firmware release archive carries them as `firmware/licenses`.

The inventory behind both indexes was taken on 6 October 2026. Each license was
read from the component's own license file or source header rather than from
package metadata. The
[licensing overview](https://github.com/tag-designs/software/blob/main/LICENSES/README.md)
describes how the notices are organized and kept current.

## Getting the source

For the programs distributed under the GPL, the complete corresponding source
is the [software repository](https://github.com/tag-designs/software) at the
release tag the package was built from — `vX.Y` for the host tools and the
flash loaders, `fw-vX.Y` for firmware images.

For the host tools that also means the third-party sources the repository
names: the vcpkg ports at the baseline recorded in `vcpkg-configuration.json`,
and Qt 6.8.2 from
[the Qt archive](https://download.qt.io/archive/qt/6.8/6.8.2/single/). For
firmware it means the [ChibiOS](https://github.com/ChibiOS/ChibiOS) submodule
at the commit that release tag records, which is also written into each image's
`*-build-manifest.json`.

Either offer is valid for at least three years from the release date, to anyone
who receives the programs.

## Hardware designs

The board and mechanical designs in the
[hardware repository](https://github.com/tag-designs/hardware) are licensed
under the CERN Open Hardware Licence Version 2 &mdash; Permissive
(`CERN-OHL-P-2.0`), Copyright &copy; 2018&ndash;2026 The Trustees of Indiana
University.

You may use, study, modify, share and distribute the designs, and make and
sell products from them, including in closed products, provided the notices
travel with the source. The designs are distributed without warranty of any
kind; the
[licence text](https://ohwr.org/cern_ohl_p_v2.txt) gives the applicable
conditions.

Of the three CERN licence variants this is the permissive one, matching the
MIT terms the software carries rather than imposing reciprocal obligations the
software side does not have. The `STM32_open_pin_data` submodule is ST's and
carries its own license.

## Citing this work

We request that any use of this work, or of derivatives of this work, in
scientific research appropriately cite our contributions in any publications.

!!! note "Citation pending"

    The preferred citation has not been settled. Until it appears here, please
    [get in touch](../contact.md) and we will tell you what to cite.
