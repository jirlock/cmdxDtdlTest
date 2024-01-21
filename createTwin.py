from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient

url = "https://recTest.api.jpe.digitaltwins.azure.net"

credential = DefaultAzureCredential()
client = DigitalTwinsClient(url, credential)

digital_twin_id = "LR15Sensor1"

temporary_twin = {
    "$metadata": {
        "$model": "dtmi:mymodel:LR15_Temperature_Sensor;1"
    },
    "$dtId": digital_twin_id,
    "name": "LR15Sensor1",
    #"area": {"$metadata":{}},
    #"capacity": {"$metadata":{}}
    "IRSensorComp": {"$metadata": {}},
    "lastKnownValue": {"$metadata": {}}
}

created_twin = client.upsert_digital_twin(digital_twin_id, temporary_twin)

print(created_twin)