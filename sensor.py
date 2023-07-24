import random
import time

from enum import Enum

from typing import Optional


class SensorType(Enum):
    LIGHT_SENSOR = 0
    TEMPERATURE_SENSOR = 1
    HUMIDITY_SENSOR = 2
    MOTION_SENSOR = 3


class SensorData:
    pass


class LightSensorData(SensorData):
    def __init__(self, val: int = 0) -> None:
        self.val = val


class TemperatureSensorData(SensorData):
    def __init__(self, val: float = 0.0) -> None:
        self.val = val


class HumiditySensorData(SensorData):
    def __init__(self, val: float = 0.0) -> None:
        self.val = val


class MotionSensorData(SensorData):
    def __init__(self, val: float = False) -> None:
        self.val = val


class Sensor:
    def __init__(self, sensor_id: int, sensor_type: SensorType) -> None:
        self.id = sensor_id
        self.type = sensor_type

        self.data: Optional[SensorData] = None

        if self.type == SensorType.LIGHT_SENSOR:
            self.data = LightSensorData()
        elif self.type == SensorType.TEMPERATURE_SENSOR:
            self.data = TemperatureSensorData()
        elif self.type == SensorType.HUMIDITY_SENSOR:
            self.data = HumiditySensorData()

    def get_data(self) -> SensorData:
        # TODO: Make this function actually linked to the sensors

        time.sleep(secs=random.uniform(0, 3))

        if self.type == SensorType.LIGHT_SENSOR:
            return LightSensorData(random.randint(0, 255))
        elif self.type == SensorType.TEMPERATURE_SENSOR:
            return TemperatureSensorData(random.uniform(0, 50))
        elif self.type == SensorType.HUMIDITY_SENSOR:
            return LightSensorData(random.uniform(0, 100))

        return None
