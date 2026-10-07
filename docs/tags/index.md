# Tag Families

A tag is a small archival data logger: it records to on-board memory and has no
radio, so the data comes back only when the bird does. What separates one
family from another is what it senses and how fast.

Three families have moved past prototype and are documented here. Others exist
in the repositories at various stages and are not covered yet.

| | [BitTag](../bittag/index.md) | [PresTag](prestag/index.md) | [IMUTag](imutag/index.md) |
| --- | --- | --- | --- |
| Senses | Movement | Barometric pressure | Movement, rotation, magnetic field, pressure |
| Records | One activity bit per second, aggregated | Pressure and temperature at a set period | Acceleration, rotation, magnetic field, pressure, temperature |
| Answers | When was the animal active? | How high was it, and when did it climb or descend? | How did it move, wingbeat by wingbeat? |
| Sample rate | 1 Hz, aggregated to 1 s – 5 min | Configurable period | 100 – 1600 Hz |
| Deployment | Up to about a year | Set by the sample period | Hours of continuous recording; months armed and waiting |
| Processor | STM32L432KC | STM32L432KC | STM32U375 |

The trade running through that table is between resolution and endurance. A
BitTag spends one bit per second and lasts a season; an IMUTag resolves
individual wingbeats and fills its flash in a day. Choosing a family is mostly
choosing where on that line a question sits.

All three are configured, armed and downloaded with the same tools, and all
three produce data in the same formats. Those are documented once, in the
[software documentation](https://tag-designs.github.io/software/user/), rather
than per family.
