from machine import Pin, I2C
import time
from I2C_LCD import I2CLcd

# Ultrasonisk sensor
trig = Pin(21, Pin.OUT)
echo = Pin(22, Pin.IN)

# LCD-oppsett
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2CLcd(i2c, i2c_addr=0x27, num_lines=2, num_columns=16)

def measure_distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()

    while echo.value() == 0:
        start = time.ticks_us()
    while echo.value() == 1:
        end = time.ticks_us()

    duration = time.ticks_diff(end, start)
    distance = (duration / 2) / 29.1  # Konverter til cm
    return distance

try:
    while True:
        distance = measure_distance()
        lcd.clear()
        lcd.putstr("Distance:")
        lcd.putstr("\n{:.2f} cm".format(distance))
        time.sleep(0.5)
except KeyboardInterrupt:
    lcd.clear()
