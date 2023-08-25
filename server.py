import random
import time
import json

from typing import List, Tuple

import sensor
from sensor import Sensor

from flask import Flask, request

app = Flask(__name__)
app.debug = True  # For debugging


sensors: List[Sensor] = [
    Sensor(
        sid=0,
        name="Light Sensor",
        room="Living Room",
        stype=sensor.SensorType.LIGHT_SENSOR,
    ),
    Sensor(
        sid=1,
        name="Temp Sensor",
        room="Garden",
        stype=sensor.SensorType.DHT11_SENSOR,
    ),
    Sensor(
        sid=2,
        name="Door",
        room="Kitchen",
        stype=sensor.SensorType.MOTION_SENSOR,
    ),
    Sensor(
        sid=3,
        name="Window",
        room="Kitchen",
        stype=sensor.SensorType.LIGHT_SENSOR,
    ),
]


# Populate sensors with data
def update_sensors(sensors: List[sensor.Sensor]):
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
    sid: int = int(request.args.get("sid", None))

    for _sensor in sensors:
        if sid == _sensor.id:
            return json.dumps(_sensor, cls=sensor.SensorEncoder)

    return "sensor_id must be supplied"


@app.route("/add_sensor", methods=["POST"])
def add_sensor() -> Tuple[str, int]:
    json_data = request.get_json(force=True)

    sid = random.randint(0, (1 << 32) - 1)
    # Name supplied can't be empty
    name = json_data.get("name", "")
    if name == "":
        return '400 Bad Request - Sensor name supplied cannot be "".', 400

    # Room supplied can't be empty
    room = json_data.get("room", "")
    if room == "":
        return '400 Bad Request - Sensor room supplied cannot be "".', 400

    # Way to check if type provided is valid without having to iterate over list
    try:
        # The type can be 0, which in python is False, but it can't be -1
        stype = sensor.SensorType(json_data.get("type", -1))
    except ValueError:
        return "400 Bad Request - Invalid sensor type supplied.", 400

    sensors.append(Sensor(sid, name, room, stype))

    return "Successfully added sensor", 200


if __name__ == "__main__":
    app.run()
