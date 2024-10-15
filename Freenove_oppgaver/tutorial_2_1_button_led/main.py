from machine import Pin
import time

led = Pin(15, Pin.OUT)
button = Pin(13, Pin.IN, Pin.PULL_UP)

try:
    while True:
        if not button.value():
            led.value(1)
        else:
            led.value(0)
finally:
    led.value(0)