#!/home/brian/mb_thermal_printer/.venv/bin/python3

from escpos.printer import File
from gpiozero import RotaryEncoder, Button
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from fonts.ttf import FredokaOne
from PIL import ImageFont
import os, random, time

# USB Printer setup
p = File("/dev/usb/lp0")
p.encoding = 'cp437'

# OLED setup
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
font16 = ImageFont.truetype(FredokaOne, 16)

# Rotary encoder: GPIO 17 = A (CLK), GPIO 27 = B (DT)
encoder = RotaryEncoder(a=17, b=27, max_steps=16, wrap=False)
button = Button(22, pull_up=True)

last_cmc = -1

def display_cmc(cmc):
    with canvas(device) as draw:
        draw.text((5, 30), f"Current CMC: {cmc}", fill="white", font=font16)

def display_print_message(cmc):
    with canvas(device) as draw:
        draw.text((5, 0), "Printing", fill="white", font=font16)
        draw.text((5, 30), f"Current CMC: {cmc}", fill="white", font=font16)

def print_random_image(cmc):
    path = f'/home/brian/mb_thermal_printer/converted_files/{cmc}/'
    try:
        image_path = os.path.join(path, random.choice(os.listdir(path)))
        p.image(image_path)
        p.textln("")
        p.textln("")
        p.textln("")
    except Exception as e:
        print(f"An error occurred: {e}")

# Track last button press for debounce
last_press_time = 0

# Main loop
while True:
    cmc = encoder.steps
    cmc = max(0, min(16, cmc))  # Clamp between 0–16

    if cmc != last_cmc:
        display_cmc(cmc)
        last_cmc = cmc

    if button.is_pressed:
        now = time.time()
        if now - last_press_time > 0.5:
            last_press_time = now
            display_print_message(cmc)
            print_random_image(cmc)

    time.sleep(0.01)
