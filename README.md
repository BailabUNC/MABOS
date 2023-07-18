# MABOS
*All work in the MABOS repository is under Copyright Protections enumerated in the LICENSE file. Please contact Arjun Putcha - arjun22@live.unc.edu - for any questions related to redistribution of this work*

*Please see [fastplotlib](https://github.com/kushalkolar/fastplotlib/tree/master), developed by Kushal Kolar, to learn more about the plotting library we primarily use.*

https://github.com/BailabUNC/MABOS/assets/96029511/9fd53396-fe4b-4406-bf57-0ea401b501d3

There are three key folders in this repository: full_design, firmware, and application.

## Full Design
This folder contains the *CAD* files (.sch and .brd) detailing schematic and layout of our pulse oximeter. It also contains a CAD library file - COMPONENTS_LIB.flbr - that has the relevant files for each component used in our design.

There is also a folder *Fab_Outputs* that contains the fabrication files necessary for laser cutting the top and bottom side of the board. *_autocad.dxf* files contain the file compatible with our laser cutter. Refer to *protocols/PCB_protocols.pdf* to follow our fabrication process.

Below is the schematic for our LED and Photodiode drivers; The 5-stage analog signal processing pipeline and led drivers are detailed in the schematic.
[embed]https://github.com/BailabUNC/MABOS/blob/master/protocols/MABOS%20Schematic.pdf[/embed]

## Firmware
There are 3 directories in this folder: Arduino, Python, and zephyr_workspace.

### Arduino
Contains the .ino file used for the adafruit_itsybitsy_nrf52840 board. The code allows for the control of 3 LED channels and 3 ADC channels. Currently, the duty cycle is set to 50%, and the acquisition rate at 100 Hz.

We also take a burst sample of each ADC (currently 5 samples) to mitigate some noise, and implement a moving average filter with a window size of 10 samples to smooth the output data.

### Python
The code here will soon be removed.

### Zephyr Workspace
Contains the source code, build files, and modified board files to use the adafruit_itsybitsy_nrf52840 board. The board files are modified to configure 3 LED and 3 ADC channels. You can reference the readme file in *firmware/zephyr_workspace* for further details on modifications made.

## Application
The *utils* folder contains the core API used to acquire, plot, and save biosensor data in real time. The *PPG Widget* python notebook utilizes the core API to operate our device. When running this script, a file named *cache.sqlite3* will be created that contains all acquired data. For our uses, we've found a minute of data acquisition corresponds to ~1 MB of data saved.

The *GUI* folder contains a QT Desktop application used solely for displaying acquired biometrics, including SpO2, Heart Rate, Respiration Rate, and Epidermal Melanin Concentration.

