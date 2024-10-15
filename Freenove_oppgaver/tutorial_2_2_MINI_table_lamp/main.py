from machine import Pin
import time

led = Pin(15, Pin.OUT)
button = Pin(13, Pin.IN, Pin.PULL_UP)

def switch():
    if led.value():
        led.value(0)
    else:
        led.value(1)

try:
    while True:
        if not button.value():
            time.sleep_ms(50)
            if not button.value():
                switch()
                while not button.value():
                    time.sleep_ms(50)
finally:
    led.value(0)
