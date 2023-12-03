from machine import Pin, I2C
from time import sleep
from bme680 import *

# ESP32 - Pin assignment
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
i2c_2 = I2C(1, sda=Pin(2), scl=Pin(3))
# ESP8266 - Pin assignment
#i2c = I2C(scl=Pin(5), sda=Pin(4))

bme = BME680_I2C(i2c=i2c)
bme2 = BME680_I2C(i2c=i2c_2)
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

print('Temperature:', result["result"][0]["temp"])
print('sensor2 temp:', result["result"][1]["temp2"])
print('Humidity:', result["result"][0]["hum"])
print('sensor2 Humidity:', result["result"][1]["hum2"])
print('Pressure:', result["result"][0]["pres"])
print('sensor2 Pressure:', result["result"][1]["pres2"])
print('Gas:', result["result"][0]["gas"])
print('sensor2 Gas:', result["result"][1]["gas2"])
print('-------')
  
  
  
