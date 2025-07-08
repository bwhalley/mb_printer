Forked 6-13-25 by @bwhalley, and updated. 

# mb_thermal_printer

Here are the scripts and steps i took to create a momir basic thermal printer, using a cheap thermal printer and a  raspberry pi

A step by step on how this was done is 

- Get the latest MTGJSON AtomicCards.json file from mtgjson.com
- Extract the scryfall id's and other useful information form the JSON file
- Get the image url's from scryfall and download them to one folder per cmc
- Using imagemagick convert the jpgs to monochrome grayscale
- Connect buttons, thermal printer and OLED screen to Raspberry Pi GPIO pins
- Add python script, and image files to Raspberry Pi
- Add python script to crontab startup so that it is automatically started when the Pi is powered on

Description of files: <br />
**get_image_urls_from_scryfall.py** - Get URLs for the actual image files from Scryfall, uses the Scryfall API and creates a new JSON file for us <br />
**download_images_from_scryfall.py** - Downloads the actual images into folders from Scryfalls database <br />
**convert_images_to_monochrome.sh** - Converts the JPG files into monochrome BMP files, this needs to be run on a Linux installation with imagemagick <br />
**momir_basic.py** - Actual python program that runs on the Pi for the printer <br />

I used the following hardware <br />
1x Rotary Encoder with push-button  <br />
1x 3 x 0.91" OLED 128 x 32 pixels I2C Screen <br />
1x Raspberry Pi 4 <br />
1x QR204 Thermal Printer <br />
1x Soldering Breadboard / Pi Hat <br />
1x USB-mini to USB-A cable (for faster communication between printer and pi) <br />
1x 16-32gb micro SD card <br />
Dupont Cables <br  />

The Raspberry Pi can run headlessly with very low power draw (~5W). The printer will idle at around 0.8W and rise to ~ 10W during printing. 

This was originally made to work with buttons instead of a rotary encoder. An encoder with push can cover the functionality in one component and much simpler wiring. The scripts contain code for managing the rotary encoder well. I also changed it from using serial over GPIO communication to USB. USB seems to print much faster than serial over GPIO. I did not investigate it overly but guess the baud rate on the printer's serial is very low as it's intended for text receipts primarily. 

Depending on your device and configuration, you may need to adjust the device names or locations in code.
