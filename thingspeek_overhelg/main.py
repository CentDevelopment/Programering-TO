import network
import urequests
import time
from ags10 import AGS10
from aht import AHT2x
from bme280_float import BME280
import machine

# Wi-Fi detaljer
SSID = "DATO IOT"
PASSWORD = "Admin:123"

# ThingSpeak detaljer
THINGSPEAK_API_KEY = "5053IZV6T4AHV0ZQ"

# Funksjon for å koble til Wi-Fi
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    print(f"Kobler til Wi-Fi: {ssid}")
    while not wlan.isconnected():
        time.sleep(1)
        print("Venter på tilkobling...")
    
    print("Wi-Fi tilkoblet!")
    print("IP-adresse:", wlan.ifconfig()[0])

# Initialiser separate I2C-busser
i2c_aht_bme = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=10000)
i2c_ags = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15), freq=10000)

# Initialiser sensorene
ags10_sensor = AGS10(i2c_ags, address=0x1A)
aht20_sensor = AHT2x(i2c_aht_bme, crc=False)
bmp280_sensor = BME280(i2c=i2c_aht_bme, address=0x77)

def read_sensors():
    try:
        tvoc = ags10_sensor.total_volatile_organic_compounds_ppb or 0
    except Exception:
        tvoc = 0
    
    if aht20_sensor.is_ready:
        temperature_aht20 = aht20_sensor.temperature or 0
        humidity = aht20_sensor.humidity or 0
    else:
        temperature_aht20 = 0
        humidity = 0
    
    try:
        bmp280_data = bmp280_sensor.read_compensated_data()
        temperature_bmp280 = bmp280_data[0] or 0
        pressure = (bmp280_data[1] / 1000) or 0
    except Exception:
        temperature_bmp280 = 0
        pressure = 0
    
    return {
        "tvoc": tvoc,
        "humidity": humidity,
        "pressure": pressure,
        "temperature_aht20": temperature_aht20,
        "temperature_bmp280": temperature_bmp280,
    }

def send_data(api_key, sensor_data):
    url = "https://api.thingspeak.com/update?api_key=" + api_key
    url += "&field1=" + str(sensor_data.get("tvoc", 0))
    url += "&field2=" + str(sensor_data.get("humidity", 0))
    url += "&field3=" + str(sensor_data.get("pressure", 0))
    url += "&field4=" + str(sensor_data.get("temperature_aht20", 0))
    url += "&field5=" + str(sensor_data.get("temperature_bmp280", 0))
    
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            print("Data sendt til ThingSpeak!")
        else:
            print(f"Feil ved sending til ThingSpeak: {response.status_code}, {response.text}")
        response.close()
    except Exception as e:
        print(f"Feil ved tilkobling til ThingSpeak: {e}")
    
    time.sleep(15)  # ThingSpeak har en grense på 15 sekunder mellom oppdateringer

# Hovedprogram
try:
    connect_to_wifi(SSID, PASSWORD)
    while True:
        sensor_data = read_sensors()
        send_data(THINGSPEAK_API_KEY, sensor_data)
        print(f"Data sendt til ThingSpeak: {sensor_data}")
        time.sleep(3600)  # Send data hver time
except KeyboardInterrupt:
    print("Avslutter programmet.")
