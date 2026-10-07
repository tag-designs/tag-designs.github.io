# PresTag

PresTag is a pressure logger. It samples barometric pressure and temperature on
a fixed schedule and writes them to on-board flash, which makes it the family
to reach for when the question is about altitude: how high a bird flew, when it
climbed or descended, and how those episodes line up with the rest of a
deployment.

It carries no accelerometer. A deployment that needs both altitude and activity
is the BitPresTag's job, which combines the two in one tag.

## What it records

| Channel | Stored as |
| --- | --- |
| Barometric pressure | Absolute pressure in mbar |
| Temperature | Degrees C, from the pressure sensor |
| Supply voltage | Tag battery voltage over the deployment |

Samples are taken at the period set in the tag configuration before
deployment, which is the main lever on how long a deployment lasts: a longer
period costs resolution and buys time.

## Hardware

The current design is the PresTagv3 board: an STM32L432KC processor, an ST
LPS27 pressure sensor, external flash, and an RV-3028 real-time clock. The
board designs live in the
[`hardware` repository](https://github.com/tag-designs/hardware) under
`BoardDesigns/Tags/PresTag`.

## Firmware variants

Two builds share the same board and report the same tag type to the monitor,
differing only in what they write:

- **PresTag** converts samples to engineering units on the tag and exports them
  as a pressure log.
- **PresTagRaw** exports raw sensor pages, converted on the host after
  download.

The build name and firmware string identify which one a tag is carrying.

## Using one

PresTag is configured, armed and downloaded with the same tools as every other
family. In Tag Monitor it presents a schedule view; there are no additional
sensor controls to set. Downloaded data arrives as a SQLite file with
`Pressure`, `Temperature` and `Voltage` tables.

[Tag Monitor reference](https://tag-designs.github.io/software/user/apps/qtmonitor.html){ .md-button }
[Log format](https://tag-designs.github.io/software/user/reference/sqlite-logs.html){ .md-button }
