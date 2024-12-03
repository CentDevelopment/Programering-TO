from machine import UART, Pin
import time

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), timeout=10)
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), timeout=10)

while True:
    input_data = input("Skriv en melding til UART1: ")
    uart1.write(input_data + '\n')
    
    time.sleep(0.1)
    
    if uart0.any() > 0:
        received_data = uart0.read().decode('utf-8').strip()
        print("Mottatt fra UART0:", received_data)
