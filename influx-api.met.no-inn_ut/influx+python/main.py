import network
import urequests
import time
from ags10 import AGS10
from aht import AHT2x
from bme280_float import BME280
import machine

# ================================
# KONFIGURASJON
# ================================

# Wi-Fi detaljer
WIFI_SSID     = "DATO IOT"
WIFI_PASSWORD = "Admin:123"

# InfluxDB detaljer
INFLUXDB_URL   = "http://10.13.37.99:8086/api/v2/write?org=vg3data&bucket=met&precision=s"
INFLUXDB_TOKEN = "SPMqvQAlKlmXV6M9VKe4sc1FJGECBsPzSR8U31NzNR8F2JGpkirh8_SoDpi2IzxUMGt9JqMQvlxBKqI5mciQUQ=="

# I2C-konfigurasjon for sensorer
I2C_AHT_BME_SDA  = 16
I2C_AHT_BME_SCL  = 17
I2C_AHT_BME_FREQ = 10000

I2C_AGS_SDA  = 14
I2C_AGS_SCL  = 15
I2C_AGS_FREQ = 10000

# Sensoradresser
AGS10_ADDRESS  = 0x1A
BME280_ADDRESS = 0x77

# Målinger for InfluxDB
INDOOR_MEASUREMENT  = "indoor_data"
OUTDOOR_MEASUREMENT = "met_data"

# MET.no API detaljer
MET_LATITUDE  = "59.2078"  # Eksempel: Kjørbekk, Skien (latitude)
MET_LONGITUDE = "9.5813"   # Eksempel: Kjørbekk, Skien (longitude)
MET_USER_AGENT = "centdevelopment.com cent@centdevelopment.com"
MET_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}".format(MET_LATITUDE, MET_LONGITUDE)

# ================================
# FUNKSJONER
# ================================

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Kobler til Wi-Fi:", ssid)
    while not wlan.isconnected():
        time.sleep(1)
        print("Venter på tilkobling...")
    print("Wi-Fi tilkoblet! IP-adresse:", wlan.ifconfig()[0])

def write_to_influxdb(measurement, tags, fields):
    tag_str = ",".join([f"{key}={value}" for key, value in tags.items()])
    field_str = ",".join([f"{key}={value}" for key, value in fields.items()])
    data = "{}{} {}".format(measurement, ("," + tag_str) if tag_str else "", field_str)
    
    headers = {
        "Authorization": f"Token {INFLUXDB_TOKEN}",
        "Content-Type": "text/plain",
    }
    try:
        response = urequests.post(INFLUXDB_URL, data=data, headers=headers)
        if response.status_code == 204:
            print(f"Data for {measurement} sendt til InfluxDB!")
        else:
            print(f"Feil ved sending til {measurement}: {response.status_code}, {response.text}")
        response.close()
    except Exception as e:
        print("Feil:", e)

def read_indoor_sensors():
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
        "temperature_aht20": temperature_aht20,
        "temperature_bmp280": temperature_bmp280,
        "pressure": pressure,
    }

def read_met_data():
    headers = {"User-Agent": MET_USER_AGENT}
    try:
        print("Henter MET.no-data...")
        response = urequests.get(MET_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            timeseries = data.get("properties", {}).get("timeseries", [])
            if timeseries:
                instant_details = timeseries[0].get("data", {}).get("instant", {}).get("details", {})
                met_fields = {
                    "air_temperature": instant_details.get("air_temperature", 0),
                    "wind_speed": instant_details.get("wind_speed", 0),
                    "wind_from_direction": instant_details.get("wind_from_direction", 0),
                    "relative_humidity": instant_details.get("relative_humidity", 0),
                    "air_pressure": instant_details.get("air_pressure_at_sea_level", 0)
                }
                print("MET.no-data hentet:", met_fields)
                response.close()
                return met_fields
            else:
                print("Ingen timeseries-data mottatt fra MET.no.")
                response.close()
                return {}
        else:
            print("Feil ved henting av MET.no-data:", response.status_code)
            response.close()
            return {}
    except Exception as e:
        print("Exception ved henting av MET.no-data:", e)
        return {}

# ================================
# INITIALISERING AV SENSORER
# ================================

# Initialiser I2C-busser for sensorene
i2c_aht_bme = machine.I2C(0, sda=machine.Pin(I2C_AHT_BME_SDA), scl=machine.Pin(I2C_AHT_BME_SCL), freq=I2C_AHT_BME_FREQ)
i2c_ags     = machine.I2C(1, sda=machine.Pin(I2C_AGS_SDA), scl=machine.Pin(I2C_AGS_SCL), freq=I2C_AGS_FREQ)

ags10_sensor  = AGS10(i2c_ags, address=AGS10_ADDRESS)
aht20_sensor  = AHT2x(i2c_aht_bme, crc=False)
bmp280_sensor = BME280(i2c=i2c_aht_bme, address=BME280_ADDRESS)

# ================================
# HOVEDPROGRAM
# ================================

try:
    connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)
    while True:
        # Les innendørs data fra sensorene
        indoor_data = read_indoor_sensors()
        # Les utendørs data fra MET.no
        met_data = read_met_data()

        # Skriv innendørs data til InfluxDB
        write_to_influxdb(
            measurement=INDOOR_MEASUREMENT,
            tags={"location": "living_room"},
            fields=indoor_data
        )

        # Skriv MET.no data til InfluxDB under eget målepunkt
        write_to_influxdb(
            measurement=OUTDOOR_MEASUREMENT,
            tags={"location": "outdoor"},
            fields=met_data
        )

        time.sleep(3600)  # Vent i en time før neste sending

except KeyboardInterrupt:
    print("Avslutter programmet.")
