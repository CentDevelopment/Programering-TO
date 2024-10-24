from machine import Pin, PWM
import time

pins = [13, 12, 11]
freq_num = 10000

pwm0 = PWM(Pin(pins[0]))
pwm1 = PWM(Pin(pins[1]))
pwm2 = PWM(Pin(pins[2]))
pwm0.freq(freq_num)
pwm1.freq(freq_num)
pwm2.freq(freq_num)

def setColor(r, g, b):
    pwm0.duty_u16(r)
    pwm1.duty_u16(g)
    pwm2.duty_u16(b)

try:
    while True:
        setColor(0, 65535, 65535)
        time.sleep(2)

        setColor(65535, 0, 65535)
        time.sleep(2)

        setColor(65535, 65535, 0)
        time.sleep(2)

except:
    pwm0.deinit()
    pwm1.deinit()
    pwm2.deinit()
