import requests
from sensor import *

# TODO: Clean up script to make it more readabel

url = "http://192.168.1.90:5000"

def sf(a: int, b: int) -> int:
    """
    Combines 2 numbers into one number, which is useful for creating ids for the
    sensor from the station id and the sensor id.
    """
    return a * a + a + b if a >= b else a + b * b


# Generate list of sensors
sensors = [
    Component(sf(0, 0), "light_sensor", "hall", ComponentType.LIGHT_SENSOR),
    Component(sf(0, 1), "dht11", "loft", ComponentType.DHT11_SENSOR),
    Component(sf(0, 2), "led", "outside", ComponentType.LED_ACTUATOR),
]

sensors[0].data.set_val(10)
sensors[1].data.set_val((41, 22))
sensors[2].data.set_val(False)


get_components = requests.get(url+"/get_components")
print("Getting all sensors")
print(get_components.text)
print()

payload = {"station_id": 0, "sensor_id": 0, "type": 1, "val": 49}
requests.post(url+"/update_sensor_value", json=payload)

payload = {"station_id": 0, "sensor_id": 67, "type": 3, "val": True}
requests.post(url+"/update_sensor_value", json=payload)

get_components = requests.get(url+"/get_components")
print("Updated sensors")
print(get_components.text)
print()

payload = {"station_id": 0, "sensor_id": 2, "type": -1}
get_components = requests.get(url+"/get_actuator_value", params=payload)


payload = {"station_id": 0, "sensor_id": 257, "type": -1}
get_components = requests.get(url+"/get_actuator_value", params=payload)

print("Adding new actuator")
print(get_components.text)


payload = {"id": sf(0, 2), "val": True}
v = requests.post(url+"/update_actuator_value", json=payload)
print(v.text)

payload = {"station_id": 0, "sensor_id": 2, "type": -1}
get_components = requests.get(url+"/get_actuator_value", params=payload)
print("Recieved actuator value")
print(get_components.text)

get_components = requests.get(url+"/get_components")
print(get_components.text)

