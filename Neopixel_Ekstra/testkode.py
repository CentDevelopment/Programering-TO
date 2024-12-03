import machine
import neopixel
import time

# Set up NeoPixel
NUM_LEDS = 4  # Number of LEDs in series
PIN = 16  # GPIO Pin 16 for NeoPixel data
np = neopixel.NeoPixel(machine.Pin(PIN), NUM_LEDS)

# Function to set a specific LED to a color
def set_single_led(index, r, g, b):
    np[index] = (r, g, b)
    np.write()

# Function to clear all LEDs (turn them off)
def clear_leds():
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()

# Function to light up LEDs one by one with a given color
def light_up_sequence(r, g, b, delay=0.1):
    for i in range(NUM_LEDS):
        set_single_led(i, r, g, b)
        time.sleep(delay)

# Test sequence
try:
    # Light up LEDs one by one in red
    light_up_sequence(255, 0, 0)
    time.sleep(1)  # Pause after completing red sequence

    # Clear LEDs before next color
    clear_leds()
    time.sleep(1)

    # Light up LEDs one by one in green
    light_up_sequence(0, 255, 0)
    time.sleep(1)  # Pause after completing green sequence

    # Clear LEDs before next color
    clear_leds()
    time.sleep(1)

    # Light up LEDs one by one in blue
    light_up_sequence(0, 0, 255)
    time.sleep(1)  # Pause after completing blue sequence

    # Turn off all LEDs
    clear_leds()

except:
    pass

finally:
    # Ensure LEDs are turned off at the end
    clear_leds()
