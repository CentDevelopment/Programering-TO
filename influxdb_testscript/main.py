import network
import urequests
import time

# Wi-Fi detaljer
SSID = "DATO IOT"
PASSWORD = "Admin:123"

# InfluxDB detaljer
INFLUXDB_URL = "http://10.13.37.99:8086/api/v2/write?org=vg3data&bucket=micropython_test&precision=s"
INFLUXDB_TOKEN = "YDDRg6Z3Zjs7kFYlYmy6K_TtZcSo5TmPy9BjAoxZjtqnj8P1bmdHYM8iklwEq19zluxx3AqiOFjJDAyUq2BnbQ=="

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
    """
    Sender et datapunkt til InfluxDB med line protocol.
    :param measurement: Målingens navn (str)
    :param tags: Ordbok med tagger (f.eks. {"location": "living_room"})
    :param fields: Ordbok med felter (f.eks. {"value": 23.5})
    """
    # Konstruer line protocol-strengen
    tag_str = ",".join([f"{key}={value}" for key, value in tags.items()])
    field_str = ",".join([f"{key}={value}" for key, value in fields.items()])
    data = f"{measurement},{tag_str} {field_str}"

    # Send forespørselen
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

# Hovedprogram
try:
    connect_to_wifi(SSID, PASSWORD)

    while True:
        # Eksempel på data som sendes til InfluxDB
        write_to_influxdb(
            measurement="temperature",
            tags={"location": "living_room"},
            fields={"value": 23.5}
        )
        time.sleep(10)  # Send data hvert 10. sekund

except KeyboardInterrupt:
    print("Avslutter programmet.")
