# Tag Configuration

To be usable, tags must be configured before "flight" and read out
afterwards. Both are done with the **Tag Monitor**, a desktop application that
talks to a tag through the USB base board.

Tag Monitor gathers metadata about a tag — its hardware and firmware
revisions, its serial number, its battery voltage — synchronizes the on-board
clock, runs the self-test, writes the schedule and sensor settings for an
experiment, and downloads the data when the tag comes back. Its Configuration
tab differs by tag family, because a BitTag, a PresTag and an IMUTag do not log
the same things.

Configurations can be saved to a file and restored, which is how a batch of
tags is given identical settings.

[Tag Monitor reference](https://tag-designs.github.io/software/user/apps/qtmonitor.html){ .md-button }

The full walkthrough — every tab, every tag family, and the configuration file
format — is in the software documentation. This page describes what the tool is
for; that one describes how to drive it.
