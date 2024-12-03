from mpu6050 import MPU6050
import time

G = 9.8
mpu = MPU6050(1, 15, 14)
mpu.MPU_Init()
time.sleep(1)

try:
    while True:
        accel = mpu.MPU_Get_Accelerometer()
        gyro = mpu.MPU_Get_Gyroscope()
        print("original data:")
        print("a/g: \tax: %d, ay: %d, az: %d\n\tgx: %d, gy: %d, gz: %d" %
              (accel[0], accel[1], accel[2], gyro[0], gyro[1], gyro[2]))
        print("calculated data:")
        print("a/g: \tax: %0.4f, ay: %0.4f, az: %0.4f\n\tgx: %0.4f, gy: %0.4f, gz: %0.4f\n" %
              (accel[0]/16384, accel[1]/16384, accel[2]/16384, gyro[0]/131, gyro[1]/131, gyro[2]/131))
        time.sleep(5)
except:
    pass
