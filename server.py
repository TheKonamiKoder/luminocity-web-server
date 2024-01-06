from typing import Dict, Tuple

from flask import Flask, request

import sensor

app = Flask(__name__)
app.debug = True  # For debugging

sensors: Dict[int, sensor.Sensor] = {}


def szudik_function(a: int, b: int) -> int:
    """
    Combines 2 numbers into one number, which is useful for creating ids for the
    sensor from the station id and the sensor id.
    """
    return a * a + a + b if a >= b else a + b * b


@app.route("/")
def home() -> Tuple[str, int]:
    return "luminocity web server", 200


@app.route("/get_sensors", methods=["GET"])
def get_all() -> Tuple[str, int]:
    """Returns all the sensors in the sensors dictionary in json form."""
    json_sensors = "["  # Returns list of sensors

    for sensor in sensors.values():
        json_sensors += sensor.to_json() + ","

    if len(sensors.values()) > 0:
        json_sensors = json_sensors[: len(json_sensors) - 1]
    json_sensors += "]"

    return json_sensors, 200


@app.route("/update_sensor_value", methods=["POST"])
def update_sensor_value() -> Tuple[str, int]:
    """
    Updates the sensor value. This function will usually be called when the sensor
    sends this request to the webserver. The function also handles adding new
    sensors to the sensors dictionary as well.
    """

    request_body = request.get_json(force=True)
    station_id = request_body.get("station_id")
    sensor_id = request_body.get("sensor_id")

    # Way to check if type provided is valid without having to iterate over list
    stype = sensor.SensorType(request_body.get("type"))
    
    
    sid = szudik_function(station_id, sensor_id)
    if not sensors.get(szudik_function(station_id, sensor_id), False):
        # Create a new sensor because it does not already exist in the database
        sensors[sid] = sensor.Sensor(
            sid=sid,
            name=str(station_id)[0:5] + "_" + str(sensor_id)[0:5],
            room="New Sensors",
            stype=stype,
        )
    
    current_sensor = sensors[sid]
    
    val = request_body.get("val")
    
    if request_body.get("type") == 1:
        val = tuple(val)
    
    current_sensor.data.set_val(val)

    return "Success - Updated sensor value!", 200


@app.route("/rename_component", methods=["POST"])
def rename_component() -> Tuple[str, int]:
    """
    Will be called by the frontend when it is necassery to rename the sensor -
    including the room as well as the component's name. It is most likely to be
    used when changing the default name of a new component to a more useful name
    by the user.
    """
    request_body = request.get_json(force=True)

    _id: int = request_body.get("id")
    name: str = request_body.get("name")
    room: str = request_body.get("room")
    
    sensors[_id].name = name
    sensors[_id].room = room

    return "Success - Renamed sensor!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
