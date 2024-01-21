from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient

def getTwin(client, name):
    get_twin = client.get_digital_twin(name)
    print(get_twin)

url = "https://recTest.api.jpe.digitaltwins.azure.net"

credential = DefaultAzureCredential()
client = DigitalTwinsClient(url, credential)

patch = [
    {
        "op": "add",
        "path": "/LR15_IRSensor_Telemetries",
        "value": {
            "arrTemp": [12.5, 16.5, 12.3, 15.5, 18.5, 13.3]
        }
    }
]

twinname = "LR15Sensor1"
compname = "IRSensorComp"

client.update_component(twinname, compname, patch)

getTwin(client, twinname)
