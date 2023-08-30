import json
import random
import time
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


@app.route("/get_all", methods=["GET"])
def get_all() -> Tuple[str, int]:
    """Returns all the sensors in the sensors dictionary in json form."""
    json_sensors = "["  # Returns list of sensors

    for sensor in sensors.values():
        json_sensors += sensor.to_json() + ","

    if len(sensors.values()) > 0: json_sensors = json_sensors[:len(json_sensors)-1]
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

    # Station ID can't be negative
    station_id = request_body.get("station_id", -1)
    if station_id < 0:
        return "400 Bad Request - Station ID supplied cannot be negative.", 400

    # Sensor ID can't be negative
    sensor_id = request_body.get("sensor_id", -1)
    if station_id < 0:
        return "400 Bad Request - Station ID supplied cannot be negative.", 400

    # Way to check if type provided is valid without having to iterate over list
    try:
        stype = sensor.SensorType(request_body.get("type", -1))
    except ValueError:
        return "400 Bad Request - Invalid sensor type supplied.", 400

    if stype == sensor.SensorType.LIGHT_SENSOR:
        # The value will never be -1
        val = request_body.get("val", -1)
        if val < 0:
            return "400 Bad Request - Light Data cannot be negative.", 400

        data: sensor.SensorData = sensor.LightSensorData(val)

    elif stype == sensor.SensorType.DHT11_SENSOR:
        # The values for temperature and humidity can't be empty
        _val: Tuple[float, float] = request_body.get("val", [None])

        try:
            _val = tuple(_val)
        except TypeError:
            return (
                "400 Bad Request - DHT11 Data must be a tuple with 2 numerical items.",
                400,
            )

        if _val := len(tuple(val)) == 2:
            if -20 <= _val[0] <= 60 and 0 <= _val[1] <= 100:
                val = _val
            else:
                return "400 Bad Request - Incorrect DHT11 Data supplied.", 400
        else:
            return (
                "400 Bad Request - DHT11 Data must be a tuple with 2 numerical items.",
                400,
            )

        data: sensor.SensorData = sensor.DHT11SensorData(val)

    elif stype == sensor.SensorType.MOTION_SENSOR:
        # The value for motion must be a boolean
        val = request_body.get("val", None)
        if not (val == True or val == False):
            return "400 Bad Request - Motion Data must be a boolean.", 400

        data: sensor.SensorData = sensor.MotionSensorData(val)

    sid = szudik_function(station_id, sensor_id)
    if s := sensors.get(szudik_function(station_id, sensor_id), False):
        s.data.set_val(data.get_val())
    else:
        # Create a new sensor because it does not already exist in the database
        sensors[sid] = sensor.Sensor(
            sid=sid,
            name=str(station_id)[0:5] + "_" + str(sensor_id)[0:5],
            room="New Sensors",
            stype=stype,
        )
        return "Success - Added new sensor!", 200

    return "Success - Updated sensor value!", 200


@app.route("/rename_sensor", methods=["POST"])
def rename_sensor() -> Tuple[str, int]:
    """
    Will be called by the frontend when it is necassery to rename the sensor -
    including the room as well as the sensor's name. It is most likely to be
    used when changing the default name of a new sensor to a more useful name
    by the user.
    """
    request_body = request.get_json(force=True)

    # Sensor's ID must be of a sensor that already exists.
    sid: int = request_body.get("id", -1)
    if not sensors.get(sid, False):
        return "400 Bad Request - Sensor ID provided does not exist.", 400

    # Sensor's name must not be empty
    name: str = request_body.get("name", "")
    if name == "":
        return "400 Bad Request - Sensor Name is not provided", 400

    # Sensor's room must not be empty
    room: str = request_body.get("room", "")
    if room == "":
        return "400 Bad Request - Sensor Room is not provided", 400

    sensors[sid].name = name
    sensors[sid].room = room
    
    return "Success - Renamed sensor!", 200


if __name__ == "__main__":
    app.run()
