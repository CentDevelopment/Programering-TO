from machine import Pin, PWM
import time

led = PWM(Pin(15))
led.freq(10000)

try:
     while True:
         for i in range(0, 65535):
             led.duty_u16(i)
             time.sleep_us(100)
         for i in range(65535, 0, -1):
             led.duty_u16(i)
             time.sleep_us(100)
finally:
    led.duty_ns(0)