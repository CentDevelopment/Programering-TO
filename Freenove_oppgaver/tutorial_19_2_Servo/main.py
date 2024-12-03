from machine import Pin, PWM, ADC
import time

servo = PWM(Pin(15))
servo.freq(50)
adc = ADC(26)

def set_servo_angle(angle):
    duty = int((angle / 180) * 5000 + 2500)
    servo.duty_u16(duty)

try:
    while True:
        adc_value = adc.read_u16()
        angle = (adc_value * 180) / 65535
        set_servo_angle(angle)
        time.sleep_ms(50)
except:
    servo.deinit()
