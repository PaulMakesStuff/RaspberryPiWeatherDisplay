#!/usr/bin/env python3

import time
import signal
import buttonshim
from weather import displayWeather
import os

def flash_led(interval, times, r, g, b):
    for i in range( times ):
        buttonshim.set_pixel(r, g, b)
        time.sleep( interval )
        buttonshim.set_pixel(0, 0, 0)
        time.sleep( interval )

def button_flash():
    flash_led(0.025, 3, 255, 255, 255)

def set_color(r, g, b):
    buttonshim.set_pixel(r, g, b)

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    set_color(255, 165, 0)
    displayWeather()
    set_color(0,0,0)

@buttonshim.on_hold(buttonshim.BUTTON_B)
def button_b_hold(button):    
    flash_led(0.025, 3, 0, 0, 255)
    os.system("sudo reboot now")

@buttonshim.on_hold(buttonshim.BUTTON_C)
def button_c_hold(button):    
    flash_led(0.025, 3, 255, 0, 0)
    os.system("sudo shutdown now")

flash_led(0.025, 3, 0, 255, 0)
set_color(255, 165, 0)
displayWeather()
set_color(0,0,0)
signal.pause()