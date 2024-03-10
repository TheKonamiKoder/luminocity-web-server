from enum import IntEnum

from typing import Tuple, Any

from abc import ABC, abstractmethod


# The ComponentType is the enum which has the types
# *Actuators must have a negative value, while sensors have a positive value*
class ComponentType(IntEnum):
    LED_ACTUATOR = -1
    
    
    LIGHT_SENSOR = 1
    DHT11_SENSOR = 2
    MOTION_SENSOR = 3


Val = Any  # Different sensors have data of different types


class ComponentData(ABC):
    @abstractmethod
    def get_val(self) -> Val:
        pass

    @abstractmethod
    def set_val(self, val: Val) -> None:
        pass
    
    @abstractmethod
    def to_json(self) -> str:
        pass

# Actuators

class LEDActuatorData(ComponentData):
    def __init__(self, val: bool = False) -> None:
        self.val = val
    
    def get_val(self) -> bool:
        return self.val
    
    def set_val(self, val: bool) -> None:
        self.val = val
        
    def to_json(self) -> str:
        return "true" if self.val else "false"

# Sensors

class LightSensorData(ComponentData):
    def __init__(self, val: int = 0) -> None:
        self.val = val

    def get_val(self) -> int:
        return self.val

    def set_val(self, val: int) -> None:
        self.val = val
        
    def to_json(self) -> str:
        return str(self.val)


class DHT11SensorData(ComponentData):
    def __init__(self, val: Tuple[float, float] = (0, 0)) -> None:
        # The first value of the tuple is the temperature and the second value is humidity
        self.val = val

    def get_val(self) -> Tuple[float, float]:
        return self.val

    def set_val(self, val: Tuple[float, float]) -> None:
        #print("The value of DHT11 is being set to (line 59) ", val)
        self.val = val

    def to_json(self) -> str:
        return f"[{self.val[0]}, {self.val[1]}]"

class MotionSensorData(ComponentData):
    def __init__(self, val: bool = False) -> None:
        self.val = val

    def get_val(self) -> bool:
        return self.val

    def set_val(self, val: bool) -> None:
        self.val = val
        
    def to_json(self) -> str:
        return "true" if self.val else "false"


class Component:
    def __init__(self, id_: int, name: str, room: str, type_: ComponentType) -> None:
        self.id = id_
        self.name = name
        self.room = room
        self.type = type_

        self.data: ComponentData = None
        
        if self.type == ComponentType.LED_ACTUATOR:
            self.data = LEDActuatorData()
        elif self.type == ComponentType.LIGHT_SENSOR:
            self.data = LightSensorData()
        elif self.type == ComponentType.DHT11_SENSOR:
            self.data = DHT11SensorData()
        elif self.type == ComponentType.MOTION_SENSOR:
            self.data = MotionSensorData()
            
    def is_sensor(self) -> bool:
        if int(self.type) > 0:      # All the sensors will have positive integer values in enum
            return True
        else:
            return False

    def to_json(self) -> str:
        """Returns a json string that shows the values of the sensor."""
        return (
            f"""
            {{
                \"id\":   {self.id},
                \"name\": \"{self.name}\",
                \"room\": \"{self.room}\",
                \"type\": {int(self.type)},
                \"val\":  {self.data.to_json()}
            }}""".replace(
                "\n", ""
            )
        )

