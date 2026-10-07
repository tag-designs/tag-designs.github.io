# IMUTag

IMUTag records how a bird moves. It writes acceleration, rotation rate,
magnetic field, barometric pressure and temperature to on-board flash fast
enough to resolve individual wingbeats, which makes it the family for questions
about flight mechanics rather than activity budgets.

Like the others it is archival: no radio, no position fix, and the tag must be
recovered to get the data. In exchange it draws almost nothing while it waits,
so a tag can sit armed for months before its recording window opens.

## At a glance

| | |
| --- | --- |
| Sample rates | 100, 200, 400, 800 or 1600 Hz, chosen before deployment |
| Channels | 3-axis acceleration, 3-axis rotation, 3-axis magnetic field, pressure, temperature |
| Storage | 2 Gbit (256 MiB) flash on the tag |
| Typical deployment | 13.7 hours of continuous recording at 400 Hz on a 12 mAh cell |
| Waiting, armed | 5.5–6.7 µA, so 74 to 91 days on a 12 mAh cell |
| Clock | ±1 ppm, about 4 ms of drift per hour |

Acceleration and rotation are recorded at the full configured rate. The
magnetometer and pressure sensor are recorded ten times less often — a
deliberate trade, since they cost current and change more slowly than a
wingbeat does. Temperature is written once per stored page.

At high rates the flash fills before the battery runs down, and at low rates
the battery goes first; the two cross near 300 Hz. Picking a sample rate is
therefore picking which limit you want to hit.

## Hardware

| Part | Role |
| --- | --- |
| STM32U375 | Reads the sensors and writes the flash |
| LSM6DSV | Accelerometer and gyroscope |
| BMM350 | Magnetometer, heading reference |
| BMP581 | Pressure and temperature |
| GD5F2GM7RE | 2 Gbit flash holding the recording |
| RV-3028-C8 | Keeps time and paces the sampling |
| TPS62840 | Makes the single 1.8 V rail everything runs from |

## Current status

The firmware runs on breakout hardware — processor, sensors and flash on a
daughter card, powered through a breakout carrying the same regulator the final
board uses. Every figure above was measured on that hardware, across a full
sweep of sample rates with verified downloads. The integrated `imutag-smps`
board has passed design checks but has not yet been fabricated, so no figure
here comes from it.

## Using one

IMUTag needs one step the other families do not: the magnetometer is calibrated
per tag, with a dedicated tool, before deployment. Otherwise it is configured
and downloaded like any other tag, and its data arrives as a SQLite file.

[IMUTag overview](https://tag-designs.github.io/software/user/imutag-overview.html){ .md-button }

That overview is the detailed version of this page: sample rates and what they
cost, resolution and noise figures, how samples are timed, the calibration and
download procedure, and an honest list of what the tag cannot yet do.
