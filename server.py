from typing import Dict, Tuple

from flask import Flask, request

import sensor
from sensor import Component, ComponentType

app = Flask(__name__)
app.debug = True  # For debugging

components: Dict[int, sensor.Component] = {
    0: Component(0, "Lamp", "Bedroom", ComponentType.LED_ACTUATOR),
    1: Component(1, "Lights", "Bedroom", ComponentType.LIGHT_SENSOR),
    2: Component(2, "Door", "Bedroom", ComponentType.MOTION_SENSOR),
    3: Component(3, "Temperature", "Bedroom", ComponentType.DHT11_SENSOR),
}

components[0].data.set_val(True)
components[1].data.set_val(235)
components[2].data.set_val(False)
components[3].data.set_val((30.10, 89.1))



def szudik_function(a: int, b: int) -> int:
    """
    Combines 2 numbers into one number, which is useful for creating ids for the
    sensor from the station id and the sensor id.
    """
    return a * a + a + b if a >= b else a + b * b


# API requests

@app.route("/")
def home() -> Tuple[str, int]:
    return "luminocity web server", 200


@app.route("/get_components", methods=["GET"])
def get_components() -> Tuple[str, int]:
    """Returns all the components in the sensors dictionary in json form."""
    json_components = "["  # Returns list of sensors

    for component in components.values():
        json_components += component.to_json() + ","

    # This just removes the last comma at the end, since JSON does not allow trailing commas
    if len(components) > 0:
        json_components = json_components[: len(json_components) - 1]
        
    json_components += "]"

    return json_components, 200


@app.route("/update_sensor_value", methods=["POST"])
def update_sensor_value() -> Tuple[str, int]:
    """
    Updates the sensor value. This function will usually be called when the sensor
    sends this request to the webserver. The function also handles adding new sensors
    to the sensors dictionary as well.
    
    Input - JSON, with parameters as shown below:
    
    {
        "station_id": (positive integer),
        "sensor_id": (positive integer),
        "type": (integer),
        "val": (value of type required by sensor type)
    }
    
    Output - "Success - Updated sensor value!"
    """

    request_body = request.get_json(force=True)
    station_id = request_body.get("station_id")
    sensor_id = request_body.get("sensor_id")

    # Way to check if type provided is valid without having to iterate over list
    type_ = sensor.ComponentType(request_body.get("type"))
    
    id_ = szudik_function(station_id, sensor_id)
    
    # Create a new sensor because it does not already exist in the database
    if not components.get(id_, False):
        components[id_] = sensor.Component(
            id_=id_,
            name=str(station_id)[0:5] + "_" + str(sensor_id)[0:5],
            room="New Sensors",
            type_=type_,
        )
    
    current_sensor = components[id_]
    
    val = request_body.get("val")
    
    # This is 
    if request_body.get("type") == sensor.ComponentType.DHT11_SENSOR:
        val = tuple(val)
    
    current_sensor.data.set_val(val)

    return "Success - Updated sensor value!", 200


@app.route("/update_actuator_value", methods=["POST"])
def update_actuator_value() -> Tuple[str, int]:
    """
    The app will be able to update the values of the actuators and then the stations
    will request to see if any changes have been made.
    """
    
    request_body = request.get_json(force=True)
    
    id_ = request_body.get("id")
    
    val = request_body.get("val")
    
    components[id_].data.set_val(val)
    
    return "Success - Updated actuator value!", 200


@app.route("/get_actuator_value", methods=["GET"])
def get_actuator_value() -> Tuple[str, int]:
    """
    The stations will request the server for any changes to the actuator (whose value
    can be cahanged based on the application with request update_actuator_value). The
    actuators will then physically change to match the data on the server. This
    function will also add actuators to the dictionary when it is first used.
    """
    
    station_id = request.args.get("station_id", type=int)
    sensor_id = request.args.get("sensor_id", type=int)
    
    type_ = sensor.ComponentType(request.args.get("type", type=int))
    
    id_ = szudik_function(station_id, sensor_id)
    
    print(station_id, sensor_id, type_, id_)
    
    if not components.get(id_, False):
        components[id_] = sensor.Component(
            id_=id_,
            name=str(station_id)[0:5] + "_" + str(sensor_id)[0:5],
            room="New Actuators",
            type_=type_            
        )
        
    print(components[id_].data.to_json())
        
    return components[id_].data.to_json(), 200
        

@app.route("/rename_component", methods=["POST"])
def rename_component() -> Tuple[str, int]:
    """
    Will be called by the frontend when it is necassery to rename the sensor - 
    including the room as well as the component's name. It is most likely to be used
    when changing the default name of a new component to a more useful name by the 
    user.
    """
    
    request_body = request.get_json(force=True)

    id_: int = request_body.get("id")
    name: str = request_body.get("name")
    room: str = request_body.get("room")
    
    components[id_].name = name
    components[id_].room = room

    return "Success - Renamed sensor!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
