import machine

i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
i2c2 = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

print('I2C H enheter', i2c.scan())
print('I2C V enheter', i2c2.scan())
