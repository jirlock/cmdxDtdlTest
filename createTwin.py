from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient
import mylib

url = "https://recTest.api.jpe.digitaltwins.azure.net"

credential = DefaultAzureCredential()
client = DigitalTwinsClient(url, credential)

sensorNames = [
    '08:3a:f2:23:cc:80',
    '08:3a:f2:22:d1:40',
    '8c:4b:14:15:94:10',
    '08:3a:f2:2b:70:ec',
    '08:3a:f2:2d:47:d0',
    '08:3a:f2:2c:58:14',
    '8c:4b:14:15:7e:84',
    '08:4b:14:15:bf:b8',
    '8c:4b:14:14:91:bc',
    '08:3a:f2:2d:47:80',
    '78:e3:6d:11:3d:20',
    '94:b9:7e:65:fc:00',
    '8c:4b:14:15:9f:dc'
]

#digital_twin_id = "LR15Sensor1"

for name in sensorNames:
    digital_twin_id = mylib.convertTopic2Id(name)
    print(digital_twin_id)
    temporary_twin = {
        "$metadata": {
            "$model": "dtmi:mymodel:LR15_Temperature_Sensor;1"
        },
        "$dtId": digital_twin_id,
        #"name": "",
        #"area": {"$metadata":{}},
        #"capacity": {"$metadata":{}}
        "IRSensorComp": {"$metadata": {}},
        "lastKnownValue": {"$metadata": {}}
    }

    created_twin = client.upsert_digital_twin(digital_twin_id, temporary_twin)
    print(created_twin)