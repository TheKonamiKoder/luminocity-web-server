
import random
import time
import json

from flask import Flask, request

app = Flask(__name__)
app.debug = True        # For debugging

class Sensor:
    def __init__(self, id: int, stype: str) -> None:
        self.id = id
        self.stype = stype
        self.data = None
    
    @staticmethod
    def get_data(sensor_id):
        time.sleep(2)
        
        return random.randint(1, 100)        

raw_data = '{"sensor1": 53, "sensor2": 43}'
data: dict = json.loads(raw_data)


@app.route('/')
def home() -> str:
    return "luminocity web server"

@app.route('/get_all')
def get_all() -> str:
    return str(data)

@app.route('/get_sensor_ids')
def get_sensor_ids() -> str:
    return str([sensor_name for sensor_name in data])

@app.route('/get_sensor_data/')
def get_with_id() -> str:
    sensor_id: str = request.args.get('sensor_id', None)
    
    if sensor_id:
        return str(data[sensor_id])
    
    return "a sensor_id must be supplied"

@app.route('/add_sensor', methods=['GET'])
def add_sensor() -> str:
    sensor_id: str = request.args.get('sensor_id', None)
    sensor_type: str = request.args.get('sensor_type', None)
    
    if sensor_id and sensor_type:
        data[sensor_id] = Sensor.get_data(sensor_id)
        
        return 'Success'
        
if __name__ == "__main__":
    app.run()