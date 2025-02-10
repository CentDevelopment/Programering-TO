import network
import urequests
import time
from ags10 import AGS10
from aht import AHT2x
from bme280_float import BME280
import machine
import thingspeak  # Importer ThingSpeak-modulen

# Wi-Fi detaljer
SSID = "DATO IOT"
PASSWORD = "Admin:123"

# InfluxDB detaljer
INFLUXDB_URL = "http://10.13.37.99:8086/api/v2/write?org=vg3data&bucket=micropython_test&precision=s"
INFLUXDB_TOKEN = "YDDRg6Z3Zjs7kFYlYmy6K_TtZcSo5TmPy9BjAoxZjtqnj8P1bmdHYM8iklwEq19zluxx3AqiOFjJDAyUq2BnbQ=="

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

# Funksjon for å sende data til InfluxDB
def write_to_influxdb(measurement, tags, fields):
    tag_str = ",".join([f"{key}={value}" for key, value in tags.items()])
    field_str = ",".join([f"{key}={value}" for key, value in fields.items()])
    data = f"{measurement},{tag_str} {field_str}"
    
    try:
        headers = {
            "Authorization": f"Token {INFLUXDB_TOKEN}",
            "Content-Type": "text/plain",
        }
        response = urequests.post(INFLUXDB_URL, data=data, headers=headers)
        if response.status_code == 204:
            print("Data sendt til InfluxDB!")
        else:
            print(f"Feil ved sending: {response.status_code}, {response.text}")
        response.close()
    except Exception as e:
        print(f"Feil: {e}")

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

# Hovedprogram
try:
    connect_to_wifi(SSID, PASSWORD)

    while True:
        sensor_data = read_sensors()
        
        # Send til InfluxDB
        write_to_influxdb(
            measurement="environment_data",
            tags={"location": "living_room"},
            fields=sensor_data
        )
        print(f"Data sendt til InfluxDB: {sensor_data}")
        
        # Send til ThingSpeak
        thingspeak.send_data(THINGSPEAK_API_KEY, sensor_data)
        print("Data sendt til ThingSpeak!")
        
        time.sleep(3600)  # Send data hver time

except KeyboardInterrupt:
    print("Avslutter programmet.")
