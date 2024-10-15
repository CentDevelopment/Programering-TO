from machine import Pin
import time

led = Pin(15, Pin.OUT)

try:
    while True:
        led.toggle()
        time.sleep(1)
finally:
    led.value(0)
