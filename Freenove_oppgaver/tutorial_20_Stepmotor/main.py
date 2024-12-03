from machine import Pin
import time

pins = [Pin(21, Pin.OUT), Pin(20, Pin.OUT), Pin(19, Pin.OUT), Pin(18, Pin.OUT)]

sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]

def step_motor(steps, delay, direction=1):
    if direction == 1:
        seq = sequence
    else:
        seq = reversed(sequence)
    for _ in range(steps):
        for step in seq:
            for pin, value in zip(pins, step):
                pin.value(value)
            time.sleep_us(delay)

try:
    while True:
        step_motor(512, 2000, direction=1)  # Full rotasjon med forsinkelse
        time.sleep(1)
        step_motor(512, 2000, direction=0)  # Rotasjon i motsatt retning
        time.sleep(1)
except KeyboardInterrupt:
    for pin in pins:
        pin.value(0)
