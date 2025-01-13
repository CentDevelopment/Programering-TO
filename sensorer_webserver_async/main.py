import machine
import network
import time
import socket
from ags10 import AGS10
from aht import AHT2x
from bme280_float import BME280

# Kobler til WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('DATO IOT', 'Admin:123')

while not sta_if.isconnected():
    time.sleep(1)
print('\nNettverkskonfigurasjon:', sta_if.ifconfig())

# Initialiser separate I2C-busser
i2c_aht_bme = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=10000)
i2c_ags = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15), freq=10000)

# Initialiser sensorene
ags10_sensor = AGS10(i2c_ags, address=0x1A)
aht20_sensor = AHT2x(i2c_aht_bme, crc=False)
bmp280_sensor = BME280(i2c=i2c_aht_bme, address=0x77)

# Globale variabler for sensorverdier
tvoc = 0
humidity = 0
pressure = 0
temperature_aht20 = 0
temperature_bmp280 = 0

# Funksjon for å lese data fra sensorene
def read_sensors():
    global tvoc, humidity, pressure, temperature_aht20, temperature_bmp280

    try:
        tvoc = ags10_sensor.total_volatile_organic_compounds_ppb
    except Exception as e:
        print(f"Error reading AGS10: {e}")
        tvoc = 0

    if aht20_sensor.is_ready:
        temperature_aht20 = aht20_sensor.temperature
        humidity = aht20_sensor.humidity

    try:
        bmp280_data = bmp280_sensor.read_compensated_data()
        temperature_bmp280 = bmp280_data[0]
        pressure = bmp280_data[1] / 1000  # Konverter hPa til kPa
    except Exception as e:
        print(f"Error reading BME280: {e}")
        pressure = 0
        temperature_bmp280 = 0

# Funksjon for å generere nettsiden
def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Raspberry Pi Pico Web Server</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="10">
        <style>
            body {{
                background-color: black;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
            }}
            h1 {{
                font-size: 24px;
                margin-top: 20px;
            }}
            table {{
                margin: 20px auto;
                border-collapse: collapse;
                width: 80%;
            }}
            td {{
                padding: 10px;
                border: 1px solid white;
                text-align: center;
            }}
            canvas {{
                margin: 20px auto;
                display: block;
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Raspberry Pi Pico Web Server</h1>
        <table>
            <tr><td>TVOC</td><td>{tvoc}</td><td>ppb</td></tr>
            <tr><td>Humidity</td><td>{humidity:.2f}</td><td>%</td></tr>
            <tr><td>Pressure</td><td>{pressure:.2f}</td><td>kPA</td></tr>
            <tr><td>Temperature (AHT20)</td><td>{temperature_aht20:.2f}</td><td>°C</td></tr>
            <tr><td>Temperature (BMP280)</td><td>{temperature_bmp280:.2f}</td><td>°C</td></tr>
        </table>
        <canvas id="sensorChart" width="400" height="200"></canvas>
        <script>
            const data = {{
                labels: ['TVOC', 'Humidity', 'Pressure', 'Temp (AHT20)', 'Temp (BMP280)'],
                datasets: [{{
                    label: 'Sensor Data',
                    data: [{tvoc}, {humidity:.2f}, {pressure:.2f}, {temperature_aht20:.2f}, {temperature_bmp280:.2f}],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }}]
            }};

            const config = {{
                type: 'bar',
                data: data,
                options: {{
                    scales: {{
                        y: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }};

            const sensorChart = new Chart(
                document.getElementById('sensorChart'),
                config
            );
        </script>
    </body>
    </html>
    """
    return html

# Setter opp socket-server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
print('Server address:', addr)

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen()

while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        request = conn.recv(1024)

        read_sensors()

        response = webpage()
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed:', e)
