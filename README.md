# Raspberry Pi Weather Display

![typical weather forecast image](background.png)

I've got this code running on a Raspberry Pi Zero W, with a button shim, and InkyPhat e-ink display.

When the script starts up it calls a display weather function which prepares an image using the Python Image Library. This image is a simple palette image, with just two colours (black and white) and it's set to the size of the InkyPhat display. I get a weather forecast using the MetOffice API and parse this, just extracting the important info - temperature, time, precipitation probability and weather type. The weather icons are selected based on the weather type. I have two sprite sheets, one for evening weather, and one for daytime weather. All of this is put into an image and sent to the e-ink display for rendering.

The button shim is simply used to enforce an update if button A is pressed. It can also shutdown the device (hold button C) or reboot (hold button B) if required. The button shim isn't required for the e-ink display, it's just nice to have when running this headless!
