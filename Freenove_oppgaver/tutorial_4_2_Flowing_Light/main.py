from machine import Pin, PWM
import time

pwm_pins = [16, 17, 18, 19, 20, 21, 22, 26, 27, 28]
pwm_channels = []

for pin in pwm_pins:
    pwm = PWM(Pin(pin))
    pwm.freq(1000)
    pwm_channels.append(pwm)

dutys = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 65535, 32768, 16384, 8192, 4096, 2048, 1024, 512, 256, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
delayTimes = 100

try:
    while True:
        for i in range(0, 20):
            for j in range(0, 10):
                pwm_channels[j].duty_u16(dutys[i+j])
            time.sleep_ms(delayTimes)

        for i in range(0, 20):
            for j in range(0, 10):
                pwm_channels[9-j].duty_u16(dutys[i+j])
            time.sleep_ms(delayTimes)

except KeyboardInterrupt:
    for pwm in pwm_channels:
        pwm.deinit()

except Exception as e:
    for pwm in pwm_channels:
        pwm.deinit()
