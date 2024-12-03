from machine import Pin
import time

sensorPin = Pin(18, Pin.IN)
ledPin = Pin(15, Pin.OUT)

try:
    while True:
        if not sensorPin.value():
            ledPin.value(1)
        else:
            ledPin.value(0)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
