import random
import time

from enum import IntEnum
from json import JSONEncoder

from typing import Optional, Tuple, Any

from abc import ABC, abstractmethod


class SensorType(IntEnum):
    LIGHT_SENSOR = 0
    DHT11_SENSOR = 1
    MOTION_SENSOR = 2


Val = Any  # Different sensors have data of different types


class SensorData(ABC):
    @abstractmethod
    def get_val(self) -> Val:
        pass

    @abstractmethod
    def set_val(self):
        pass


class LightSensorData(SensorData):
    def __init__(self, val: int = 0) -> None:
        self.val = val

    def get_val(self) -> int:
        return self.val

    def set_val(self, val: int) -> None:
        self.val = val


class DHT11SensorData(SensorData):
    def __init__(self, val: Tuple[float, float] = (0, 0)) -> None:
        # The first value of the tuple is the temperature and the second value is humidity
        self.val = val

    def get_val(self) -> Tuple[float, float]:
        return self.val

    def set_val(self, val: Tuple[float, float]) -> None:
        self.val = val


class MotionSensorData(SensorData):
    def __init__(self, val: bool = False) -> None:
        self.val = val

    def get_val(self) -> bool:
        return self.val

    def set_val(self, val: bool) -> None:
        self.val = val


class Sensor:
    def __init__(self, sid: int, name: str, room: str, stype: SensorType) -> None:
        self.id = sid
        self.name = name
        self.room = room
        self.type = stype

        self.data: Optional[SensorData] = None

        if self.type == SensorType.LIGHT_SENSOR:
            self.data = LightSensorData()
        elif self.type == SensorType.DHT11_SENSOR:
            self.data = DHT11SensorData()
        elif self.type == SensorType.MOTION_SENSOR:
            self.data = MotionSensorData()

    def to_json(self) -> str:
        """Returns a json string that shows the values of the sensor."""
        return f"""
            {{
                id:   {self.id},
                name: {self.name},
                room: {self.room},
                type: {int(self.type)},
                val:  {self.data.get_val()}
            }}""".replace(
            "\n", ""
        )  # Gets rid of the newlines, so that when displaying it is easier.
