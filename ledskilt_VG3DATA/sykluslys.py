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

# Lysstyrke
BRIGHTNESS = 0.1

# Funksjon for å sette farge på hele LED-stripen med redusert lysstyrke
def set_color(r, g, b, brightness=BRIGHTNESS):
    scaled_r = int(r * brightness)
    scaled_g = int(g * brightness)
    scaled_b = int(b * brightness)
    for i in range(NUM_LEDS):
        np[i] = (scaled_r, scaled_g, scaled_b)
    np.write()

# Funksjon for å slå av alle lys
def clear():
    set_color(0, 0, 0)

# Syklus 1: Rullende regnbue
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

# Funksjon for å generere farger til regnbue
def wheel(pos):
    pos = 255 - pos
    if pos < 85:
        return (255 - pos * 3, 0, pos * 3)
    if pos < 170:
        pos -= 85
        return (0, pos * 3, 255 - pos * 3)
    pos -= 170
    return (pos * 3, 255 - pos * 3, 0)

# Syklus 2: Pulserende rødt
def pulsing_red(duration=10):
    start_time = time.time()
    while time.time() - start_time < duration:
        for brightness in range(0, 101, 5):
            set_color(255, 0, 0, brightness / 100 * BRIGHTNESS)
            time.sleep(0.05)
        for brightness in range(100, -1, -5):
            set_color(255, 0, 0, brightness / 100 * BRIGHTNESS)
            time.sleep(0.05)
    clear()

# Syklus 3: Løpende grønt lys
def running_green(duration=10):
    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(NUM_LEDS):
            np[i] = (0, int(255 * BRIGHTNESS), 0)
            np.write()
            time.sleep(0.01)
            np[i] = (0, 0, 0)
    clear()

# Syklus 4: Blinkende lys
def blinking_lights(duration=10):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    start_time = time.time()
    while time.time() - start_time < duration:
        for color in colors:
            set_color(*color, brightness=BRIGHTNESS)
            time.sleep(0.5)
            clear()
            time.sleep(0.5)
    clear()

# Hovedloop
while True:
    rolling_rainbow()
    time.sleep(1)
    pulsing_red()
    time.sleep(1)
    running_green()
    time.sleep(1)
    blinking_lights()
    time.sleep(1)

    # Blått lys i 10 sekunder før restart
    set_color(0, 0, 255, brightness=BRIGHTNESS)
    time.sleep(10)
    clear()
