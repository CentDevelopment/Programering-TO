import machine
import neopixel
import time

# Konfigurer WS2812B LED-stripen
LED_PIN = 15         # GPIO 15 til DIN på LED-stripen
NUM_LEDS = 360       # Antall LEDs på stripen
np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)

# Konfigurer innebygd LED (GPIO 25)
onboard_led = machine.Pin(25, machine.Pin.OUT)
onboard_led.value(1)  # Slå på innebygd LED

# Funksjon for å sette en spesifikk LED til en valgt farge
def set_single_led(index, r, g, b, brightness=1.0):
    """
    Setter en spesifikk LED på stripen til en valgt farge.

    Args:
        index (int): Indeksen til LED-en (0-baserte indeks).
        r (int): Rød verdi (0-255).
        g (int): Grønn verdi (0-255).
        b (int): Blå verdi (0-255).
        brightness (float): Lysstyrke (0.0 til 1.0). Standard er 1.0 (full lysstyrke).
    """
    if 0 <= index < NUM_LEDS:  # Sjekk at indeksen er gyldig
        scaled_r = int(r * brightness)
        scaled_g = int(g * brightness)
        scaled_b = int(b * brightness)
        np[index] = (scaled_r, scaled_g, scaled_b)
        np.write()
    else:
        print(f"Feil: Indeks {index} er utenfor rekkevidde. Tillatte verdier: 0-{NUM_LEDS-1}")

# Testsekvens
while True:
    set_single_led(10, 255, 0, 0, brightness=0.5)  # LED 10 til rød, 50% lysstyrke
    time.sleep(5)
    set_single_led(10, 0, 255, 0, brightness=0.5)  # LED 10 til grønn, 50% lysstyrke
    time.sleep(5)
    set_single_led(10, 0, 0, 255, brightness=0.5)  # LED 10 til blå, 50% lysstyrke
    time.sleep(5)
    set_single_led(10, 0, 0, 0)  # Slukk LED 10
    time.sleep(5)
