from machine import Pin
import time

led = Pin(15, Pin.OUT)
button = Pin(13, Pin.IN, Pin.PULL_UP)

try:
    while True:
        if not button.value():
            time.sleep_ms(50)
            if not button.value():
                led.toggle()
                while not button.value():
                    time.sleep_ms(50)
finally:
    led.value(0)

