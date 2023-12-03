import network
import socket
import uwebsocket as websocket
from machine import Pin, I2C
from bme680 import *

def web_page(result):
    html = """<html>
<head>
    <title>ESP with BME680</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
        body {
            text-align: center;
            font-family: "Trebuchet MS", Arial;
        }
        table {
            border-collapse: collapse;
            margin-left:auto;
            margin-right:auto;
        }
        th {
            padding: 12px;
            background-color: #0043af;
            color: white;
        }
        tr {
            border: 1px solid #ddd;
            padding: 12px;
        }
        tr:hover {
            background-color: #bcbcbc;
        }
        td {
            border: none;
            padding: 12px;
        }
        .sensor {
            color:white;
            font-weight: bold;
            background-color: #bcbcbc;
            padding: 1px;
        }
    </style>
</head>
<body>
    <h1>bha ESP with BME680</h1>
    <table>
        <tr><th>MEASUREMENT</th><th>VALUE</th></tr>
        <tr><td>Temp. Celsius</td><td><span class="sensor">%TEMP_C%</span></td></tr>
        <tr><td>Temp. Fahrenheit</td><td><span class="sensor">%TEMP_F%</span></td></tr>
        <tr><td>Pressure</td><td><span class="sensor">%PRESSURE%</span></td></tr>
        <tr><td>Humidity</td><td><span class="sensor">%HUMIDITY%</span></td></tr>
        <tr><td>Gas</td><td><span class="sensor">%GAS%</span></td></tr>
    </table>
</body>
</html>"""
    return html.replace('%TEMP_C%', str(result["result"][0]["temp"])) \
               .replace('%TEMP_F%', str(result["result"][0]["temp"] * (9/5) + 32)) \
               .replace('%PRESSURE%', str(result["result"][0]["pres"])) \
               .replace('%HUMIDITY%', str(result["result"][0]["hum"])) \
               .replace('%GAS%', str(result["result"][0]["gas"]))

def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    
    while not ap.active():
        pass
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        try:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            print('Content = %s' % str(request))

            # Check if the request is for WebSocket upgrade
            if 'Upgrade: websocket' in str(request):
                ws = websocket.server_handshake(conn)
                websocket_server(ws, result)
            else:
                response = web_page(result)
                conn.send(response)
            conn.close()
        except Exception as conn_error:
            print(f"An error occurred while handling connection: {conn_error}")

# Initialize BME680 sensors
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
i2c_2 = I2C(1, sda=Pin(2), scl=Pin(3))
bme = BME680_I2C(i2c=i2c)
bme2 = BME680_I2C(i2c=i2c_2)

# Read sensor data
data = [
    {
        "temp": round(bme.temperature, 2),
        "pres": round(bme.pressure, 2),
        "hum": round(bme.humidity, 2),
        "gas": round(bme.gas/1000, 2),
    },
    {
        "temp2": round(bme2.temperature, 2),
        "pres2": round(bme2.pressure, 2),
        "hum2": round(bme2.humidity, 2),
        "gas2": round(bme2.gas/1000, 2),
    },
]

result = {"result": data}

# Start access point mode
ap_mode('Rasberrywifi', 'PASSWORD')

