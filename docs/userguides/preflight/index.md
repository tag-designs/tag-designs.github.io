# Preparing for Flight

Preparing BitTags for flight requires the following steps:

1.  Charging -- be prepared to charge each tag for at least 2 days
2.  Configuring -- the data collection protocol including start/end times, hibernation periods, and sensor parameters.
3.  Insulating -- after configuration the test points should be immediately covered with insulating tape
4.  Harness attachment

In this guide we discuss 1-3.  **Note** some of the photos were made with earlier versions of the tags and tag bases; however, the principles remain the same.

## Visual Glossary

### Bit Tags

<div class="grid" markdown>

<div markdown>

Ultra-low power reusable accelerometer loggers, capable of logging  activity up to a year

</div>

<div markdown>

![](./images/image42.jpg)

</div>

<div markdown>

![](./images/image37.jpg)

</div>

</div>


### Charger Bases

<div class="grid" markdown>

<div markdown>

Charges Bit Tag batteries and displays battery charge status.

</div>

<div markdown>

![](./images/image30.jpg)

</div>

</div>

### Programmer Base

<div class="cf" markdown>

<div class="fr w-50" markdown>

![](./images/image17.jpg)

</div>


Allows data transfer between Bit Tags and computer, for configuration
and data downloading

</div>


###  Mini-USB Cable


<div class="grid" markdown>

<div markdown>

Delivers power and data to Bit Tag chargers and programming base.

</div>

<div markdown>

![](./images/image44.jpg)

</div>

</div>

### Insulating Tape (3mm Kapton)

<div class="grid" markdown>

<div markdown>

Protects Bit Tag contacts from short-circuits.

</div>

<div markdown>

![](./images/image28.jpg)

</div>

</div>

###  Tape Application Sticks (4mm width)

<div class="grid" markdown>

<div markdown>

Flat wooden sticks, commonly used as coffee stirrers. Useful for
applying tape to Bit Tags, and for measuring tape length.

</div>

<div markdown>

![](./images/image23.jpg)

</div>

</div>

###  Harness Material

<div class="grid" markdown>

<div markdown>

Elastic sewing thread.  May also be available through dental supply houses.

</div>

<div markdown>

![](./images/image36.jpg)

</div>

</div>

###  Scissors

<div class="grid" markdown>

<div markdown>

For cutting tape and harness material. The smaller the better.

</div>

<div markdown>

![](./images/image27.jpg)

</div>

</div>

### Monitor Program

<div class="grid" markdown>

<div markdown>

Configures and downloads data from BitTag.

[Tag Monitor reference](https://tag-designs.github.io/software/user/apps/qtmonitor.html)

</div>

<div markdown>

![](./images/image40.png)

</div>

</div>

###  btviz Program

<div class="grid" markdown>

<div markdown>

Displays data and generates actograms.

[Bit Tag Visualizer reference](https://tag-designs.github.io/software/user/apps/btdataviz.html)

</div>

<div markdown>

![](./images/image7.png)

</div>

</div>
 

## BitTags
--------

<div class="grid" markdown>

<div markdown>

![](./images/image20.jpg)

</div>

<div markdown>

![](./images/image21.jpg)

</div>

</div>

### Specifications

-   Weight (Without Harness) **0.64g**

-   Dimensions **22Lx9Wx6H mm**

-   Run Time (Depends on mode, limited by battery size)

    -   Bits Per Second **239 hours (\~10 days)**

    -   Counts per Minute **2395 hours (\~100 days)**

    -   Counts per 4 Minutes **9900 hours (\~414 days)**

    -   Counts per 5 Minutes **8700 hours (\~362 days)**

-   Battery Capacity **5.5 mAh**

-   Average Current Consumption **\< 1uA**

-   CPU **STM32L432KC**

-   Accelerometer **ADXL362**

-   Clock Accuracy **±3ppm**

## Pre-Flight

### 1. Charge Bit Tags

<div class="grid" markdown>

<div markdown>

Plug in Charger Base and ensure it is receiving power. A green light will illuminate on the Charger Base that is plugged in.  All other Charger Bases can then share power from this Charger Base.

</div>

<div markdown>

![](./images/image18.jpg)

</div>

</div>

<div class="grid" markdown>

<div markdown>

Remove nuts and lid from Charger Base

</div>

<div markdown>

![](./images/image41.jpg)

</div>

</div>

<div class="grid" markdown>

<div markdown>

Place Bit Tag in the plastic holder, ensuring it seats fully.

</div>

<div markdown>

![](./images/image38.jpg)

</div>

</div>

<div class="grid" markdown>

<div markdown>

Place lid on base, aligning dots.

</div>

<div markdown>

![](./images/image24.jpg)

</div>

</div>

<div class="grid" markdown>

<div markdown>

Gently tighten nuts with one finger, to avoid damaging delicate electronics.

</div>

<div markdown>

![](./images/image33.jpg)

</div>

</div>

<div class="grid" markdown>

<div markdown>

* Check to make sure BitTag makes contact with charger.
* Bit Tags typically take 48-27 hours to charge.
* Charging is **Not** complete when the battery indicator turns from red to green.  To fully charge, batteries must be held at their charge voltage for 24-48 hours.

</div>

<div markdown>

![](./images/image13.jpg)
 ![](./images/image12.jpg)

</div>

</div>


* Remove Bit Tags when done charging. Unused Bit Tags can store  for 1-2 months before needing to be recharged.

* To remove, reverse the installation process.

### 2. Configure Bit Tags

**Note: Images in this section need updating for newer software**

<div class="grid" markdown>

<div markdown>

Place Bit Tag in Programmer Base, following the same procedure as installing Bit Tags into chargers.
**Note:** Programmer Base must be plugged into computer before receiving a Bit Tag.

</div>

<div markdown>

![](./images/image38.jpg)

</div>

</div>

<div class="grid" markdown>

<div markdown>

* Open the [monitor program](https://tag-designs.github.io/software/user/apps/qtmonitor.html).
* Click "Attach"
* Check that battery voltage is **3.0 volts** or greater. If not, detach and recharge. While still functional, battery voltage below 3.0 volts will result in suboptimal runtimes.

</div>

<div markdown>

![](./images/image11.png)

![](./images/image1.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

* If Bit Tag is in a state other than "IDLE", you may need to "Stop" and then "Erase" Bit Tag.

</div>

<div markdown>

![](./images/image3.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

* Once the tag is in the "idle" state, run the internal tests ("Test") and then synchronize the clock "Sync".
* If any tests fail, you should not use the tag.

</div>

<div markdown>

![](./images/image25.png)
![](./images/image5.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

* Click into the "Configure" tab.
* Schedule BitTag Data Collection

</div>

<div markdown>

![](./images/image35.png)
![](./images/image6.png)

</div>

</div>
<div class="grid" markdown>

<div markdown>

* Select Data Type Log Format based upon experiment requirements
    1.  **Activity Bit Per Second**: Gives second-by-second log of whether or not the animal is active. Highest resolution data. Run Time of around **10 days**.
    2.  **Activity Bit Count Per Minute**: Records the percentage of each minute the animal was active. Run Time of around **100 days**.
    3.  **Activity Bit Count Per Four/Five Minutes**: Same as Activity Bit Count Per Minute, but over four or five minute intervals. Lowest resolution, but allows Run
    Time of around **365 days**.

</div>

<div markdown>

![](./images/image34.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

Click "Run" to save settings and start Bit Tag.

</div>

<div markdown>

![](./images/image19.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

Return to the "Tag State" tab.
Ensure that the Bit Tag is in the "CONFIGURED" or "RUNNING" state. If not, check your configuration and click "Run" again.

</div>

<div markdown>

![](./images/image4.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

Click "Detach" and  remove BitTag from base.

</div>

<div markdown>

![](./images/image2.png)

</div>

</div>

### 3. Insulate Bit Tags

<div class="grid" markdown>

<div markdown>

Cut a short strip of Insulating Tape just long enough to fully cover contacts (about 4mm - or the width of tape application sticks) on the back of Bit Tag.

</div>

<div markdown>

![](./images/image22.jpg)
![](./images/image14.jpg)

</div>

</div>

<div class="grid" markdown>

<div markdown>

Place tape partially on Tape Application Stick (leaving \~2mm overhang lengthwise) 
and gently stick one edge onto Bit Tag

</div>

<div markdown>

![](./images/image43.jpg)

</div>

</div>

<div class="grid" markdown>

<div markdown>

Press stick firmly onto tape and "squeegee" out any air bubbles or pockets. Tape should sit flat on surface of Bit Tag.

</div>

<div markdown>

![](./images/image31.jpg)

</div>

</div>

### 4 Build Harnesses

See section ???

<div class="grid" markdown>

<div markdown>

Bit Tags can be attached via harness using the four mounting holes (1mm diameter).
For songbird, the size of the leg-loop harness can be estimated using the function described by Naef-Daenzer (2007, J. Avian Biology, 38: 404-407)

</div>

<div markdown>

![](./images/image29.jpg)

</div>

</div>

## Post-Processing

### 1 Recovery

<div class="grid" markdown>

<div markdown>

Remove harnesses and insulating tape, being careful not to contact the Bit Tag with sharp or metallic tools.
The Tape Application Stick can also be used to gently peel up the tape.

</div>

<div markdown>

![](./images/image45.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

* Place Bit Tag into Programmer Base.
  -   Note: Ensure Programmer Base is plugged into the computer first.
* Open the [monitor program](https://tag-designs.github.io/software/user/apps/qtmonitor.html) and attach.

</div>

<div markdown>

![](./images/image11.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

Stop the BitTag.

</div>

<div markdown>

![](./images/image26.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

* Save data. **Important:** Save your data as a ".txt" file.
    - **Note: The data length may sometimes show up as zero, even if there is saved data onboard.**
* Detach the BitTag and remove from base.

</div>

<div markdown>

![](./images/image15.png)

</div>

</div>

### 2 Data Visualization

The steps below cover the common case. For the full guide -- filtering,
actograms, sun elevation and export -- see the
[Bit Tag Visualizer reference](https://tag-designs.github.io/software/user/apps/btdataviz.html).


<div class="grid" markdown>

<div markdown>

* Open [btviz](https://tag-designs.github.io/software/user/apps/btdataviz.html)

* To import data click 'load' and select data file (data file should have a .txt extension)

</div>

<div markdown>

![](./images/image8.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

If you need to trim your data, enter Start and End times then click "Zoom"

</div>

<div markdown>

![](./images/image39.png)

</div>

</div>

<div class="grid" markdown>

<div markdown>

You may also use your mouse to visually select these times:

1.  Double-click on the chart with the Left Mouse Button to set the Start time (One-finger double-click on Mac).

2.  Double-click on the chart with the Right Mouse Button to set the End time (Double-click with two fingers, or while holding Control (⌃) on Mac).
3.  Click "Zoom"

</div>

<div markdown>

![](./images/image9.png)

</div>

</div>


<div class="grid" markdown>

<div markdown>

You may export your data in a variety of formats:
* **PDF/PNG**: Saves the currently displayed figure as an image
* **CSV**: Saves all data currently visible in the image as a .csv file of data points.

</div>

<div markdown>

![](./images/image32.png)

</div>

</div>


<div class="grid" markdown>

<div markdown>

You may also view and save actograms by clicking on the 'actogram' tab at the top.

</div>

<div markdown>

![](./images/image10.png)

</div>

</div>


