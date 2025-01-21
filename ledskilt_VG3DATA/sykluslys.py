import machine
import neopixel
import time
import random

LED_PIN = 15
NUM_LEDS = 360
np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)
BRIGHTNESS_DEFAULT = 0.4
BRIGHTNESS_RED = 0.6
COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "yellow": (255, 255, 0),
    "white": (255, 255, 255)
}

def set_color(r, g, b, brightness=BRIGHTNESS_DEFAULT):
    scaled_r = int(r * brightness)
    scaled_g = int(g * brightness)
    scaled_b = int(b * brightness)
    for i in range(NUM_LEDS):
        np[i] = (scaled_r, scaled_g, scaled_b)
    np.write()

def clear():
    set_color(0, 0, 0)

def rolling_rainbow(duration=10):
    start_time = time.time()
    while time.time() - start_time < duration:
        for j in range(256):
            if time.time() - start_time >= duration:
                break
            for i in range(NUM_LEDS):
                np[i] = wheel((i + j) & 255)
            np.write()
            time.sleep(0.05)
    clear()

def wheel(pos):
    pos = 255 - pos
    if pos < 85:
        return (255 - pos * 3, 0, pos * 3)
    if pos < 170:
        pos -= 85
        return (0, pos * 3, 255 - pos * 3)
    pos -= 170
    return (pos * 3, 255 - pos * 3, 0)

def pulsing_colors(duration=5):
    start_time = time.time()
    color_list = list(COLORS.values())
    color = random.choice(color_list)
    while time.time() - start_time < duration:
        brightness = 0
        increasing = True
        while True:
            set_color(*color, brightness / 100 * BRIGHTNESS_DEFAULT)
            time.sleep(0.01)
            if increasing:
                brightness += 1
                if brightness >= 100:
                    increasing = False
            else:
                brightness -= 1
                if brightness <= 0:
                    break
    clear()

def running_multicolor_bounce_45_led(duration=10):
    start_time = time.time()
    color_list = list(COLORS.values())
    color = random.choice(color_list)
    while time.time() - start_time < duration:
        for i in range(NUM_LEDS - 45):
            for j in range(45):
                np[i + j] = tuple(int(c * BRIGHTNESS_DEFAULT) for c in color)
            np.write()
            time.sleep(0.000025)
            for j in range(45):
                np[i + j] = (0, 0, 0)

        for i in range(NUM_LEDS - 45, -1, -1):
            for j in range(45):
                np[i + j] = tuple(int(c * BRIGHTNESS_DEFAULT) for c in color)
            np.write()
            time.sleep(0.000025)
            for j in range(45):
                np[i + j] = (0, 0, 0)
    clear()

def running_light_with_trail_multicolor(duration=10):
    start_time = time.time()
    color_list = list(COLORS.values())
    color = random.choice(color_list)
    while time.time() - start_time < duration:
        for i in range(NUM_LEDS):
            np[i] = tuple(int(c * BRIGHTNESS_DEFAULT) for c in color)
            np.write()
            time.sleep(0.01)

        for i in range(NUM_LEDS - 1, -1, -1):
            np[i] = (0, 0, 0)
            np.write()
            time.sleep(0.01)
    clear()

# Hovedloop
while True:
    rolling_rainbow()
    time.sleep(0.1)
    pulsing_colors()
    time.sleep(0.1)
    running_multicolor_bounce_45_led()
    time.sleep(0.1)
    running_light_with_trail_multicolor()
    time.sleep(0.1)

    # Blått lys i 10 sekunder før restart
    set_color(0, 0, 255, brightness=BRIGHTNESS_DEFAULT)
    time.sleep(10)
    clear()