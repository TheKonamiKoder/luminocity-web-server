import random
import time
import json

from typing import List

import sensor

from flask import Flask, request

app = Flask(__name__)
app.debug = True  # For debugging


sensors: List[sensor.Sensor] = [
    sensor.Sensor(
        sid=0,
        name="Light Sensor",
        room="Living Room",
        stype=sensor.SensorType.LIGHT_SENSOR,
    ),
    sensor.Sensor(
        sid=1,
        name="Temp Sensor",
        room="Garden",
        stype=sensor.SensorType.TEMPERATURE_SENSOR,
    ),
    sensor.Sensor(
        sid=2,
        name="Humidity Sensor",
        room="Kitchen",
        stype=sensor.SensorType.HUMIDITY_SENSOR,
    ),
]

# Populate sensors with data
for _sensor in sensors:
    _sensor.get_data()


@app.route("/")
def home() -> str:
    return "luminocity web server"


@app.route("/get_all")
def get_all() -> str:
    return json.dumps(sensors, cls=sensor.SensorEncoder)


@app.route("/get_sensor_ids")
def get_sensor_ids() -> str:
    return str([_sensor.id for _sensor in sensors])


@app.route("/get_sensor_data")
def get_with_id() -> str:
    sensor_id: str = request.args.get("sensor_id", None)

    if sensor_id:
        return str(data[sensor_id])

    return "sensor_id must be supplied"


@app.route("/add_sensor", methods=["UPDATE"])
def add_sensor() -> str:
    sid: str = request.args.get("sid", None)
    name: str = request.args.get("name", None)
    room: str = request.args.get("room", None)
    stype: str = request.args.get("stype", None)

    if sid and name and room and stype:
        for _stype in sensor.SensorType:
            if _stype.name == stype:
                __stype = _stype

        sensors.append(sensor.Sensor(int(sid), name, room, __stype))

        return "success"
    else:
        return "error - all parameters not supplied"


if __name__ == "__main__":
    app.run()
