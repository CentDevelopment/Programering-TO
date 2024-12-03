from machine import Pin
import time

# Definer pinner
button = Pin(16, Pin.IN, Pin.PULL_UP)  # Knapp med pull-up
transistor = Pin(15, Pin.OUT)         # GPIO som styrer transistoren

try:
    while True:
        if not button.value():  # Når knappen trykkes (lavt signal)
            transistor.value(1)  # Aktiver NPN-transistoren (buzzer ON)
            print("Button released! Buzzer ON.")
        else:
            transistor.value(0)  # Deaktiver NPN-transistoren (buzzer OFF)
            print("Button pressed! Buzzer OFF.")
        time.sleep(0.1)  # Debounce
except KeyboardInterrupt:
    print("Program stopped.")
    transistor.value(0)  # Slå av transistoren ved avslutning
