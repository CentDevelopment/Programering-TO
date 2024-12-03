import machine
import neopixel
import time

# Konfigurer WS2812B LED-stripen
LED_PIN = 15         # GPIO 15 til DIN på LED-stripen
NUM_LEDS = 432       # Antall LEDs på stripen
np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)

# Konfigurer innebygd LED (GPIO 25)
onboard_led = machine.Pin(25, machine.Pin.OUT)
onboard_led.value(1)  # Slå på innebygd LED

# Funksjon for å sette farge på LED-stripen med redusert lysstyrke
def set_color(r, g, b, brightness=0.1):
    scaled_r = int(r * brightness)
    scaled_g = int(g * brightness)
    scaled_b = int(b * brightness)
    for i in range(NUM_LEDS):
        np[i] = (scaled_r, scaled_g, scaled_b)
    np.write()

# Testsekvens
while True:
    set_color(255, 0, 0, brightness=0.1)  # Rød, 10% lysstyrke
    time.sleep(5)
    set_color(0, 255, 0, brightness=0.1)  # Grønn, 10% lysstyrke
    time.sleep(5)
    set_color(0, 0, 255, brightness=0.1)  # Blå, 10% lysstyrke
    time.sleep(5)
    set_color(0, 0, 0)                    # Slukk
    time.sleep(5)
