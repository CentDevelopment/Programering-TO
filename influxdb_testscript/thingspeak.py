import urequests
import time

def send_data(api_key, sensor_data):
    """
    Sender sensorverdier til ThingSpeak.
    :param api_key: ThingSpeak API-nøkkel (str)
    :param sensor_data: Ordbok med sensorverdier
    """
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