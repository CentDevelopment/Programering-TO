from machine import Pin, PWM
import time

pins = [13, 12, 11]

pwmC = PWM(Pin(pins[0]))
pwmP = PWM(Pin(pins[1]))
pwmY = PWM(Pin(pins[2]))
pwmC.freq(1000)
pwmP.freq(1000)
pwmY.freq(1000)

def setColor(r, g, b):
    pwmY.duty_u16(int(r * 65535 / 255))
    pwmC.duty_u16(int(g * 65535 / 255))
    pwmP.duty_u16(int(b * 65535 / 255))

def gradvisendring(startColor, endColor, steps, delay):
    r1, g1, b1 = startColor
    r2, g2, b2 = endColor
    for i in range(steps):
        r = r1 + (r2 - r1) * i // steps
        g = g1 + (g2 - g1) * i // steps
        b = b1 + (b2 - b1) * i // steps
        setColor(r, g, b)
        time.sleep_ms(delay)

try:
    while True:
        gradvisendring((255, 0, 255), (255, 255, 0), 255, 50)
        gradvisendring((255, 255, 0), (0, 255, 255), 255, 50)
        gradvisendring((0, 255, 255), (255, 0, 255), 255, 50)

except:
    pwmC.deinit()
    pwmP.deinit()
    pwmY.deinit()
