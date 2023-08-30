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
    return a * a + a + b if a >= b else a + b * b


# Populate sensors with data
def update_sensors(sensors: Dict[int, sensor.Sensor]):
    for i in range(len(sensors)):
        sensors[i].update_data()


@app.route("/")
def home() -> str:
    return "luminocity web server"


@app.route("/get_all", methods=["GET"])
def get_all() -> str:
    update_sensors(sensors)
    return json.dumps(sensors, cls=sensor.SensorEncoder)


@app.route("/get_sensor_ids", methods=["GET"])
def get_sensor_ids() -> str:
    return str([_sensor.id for _sensor in sensors])


@app.route("/get_sensor_data", methods=["GET"])
def get_with_id() -> str:
    sid = int(request.args.get("sid", None))

    for _sensor in sensors:
        if sid == _sensor.id:
            return json.dumps(_sensor, cls=sensor.SensorEncoder)

    return "sensor_id must be supplied"

@app.route("/update_sensor_value", methods=["POST"])
def update_sensor_value() -> Tuple[str, int]:
    """
    Updates the sensor value. This function will usually be called when the sensor sends
    this request to the webserver. The function also handles adding new sensors to the sensors
    dictionary as well.
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
        sensors[sid] = sensor.Sensor(
            sid=sid,
            name=str(station_id) + "_" + str(sensor_id),
            room="New Sensors",
            stype=stype,
        )


if __name__ == "__main__":
    app.run()
