from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient

def getTwin(client, name):
    get_twin = client.get_digital_twin(name)
    print(get_twin)

url = "https://15LectureRoom.api.jpe.digitaltwins.azure.net"

credential = DefaultAzureCredential()
client = DigitalTwinsClient(url, credential)

patch = [
    {
        "op": "add",
        "path": "/floorInfo",
        "value": {
            "maxFloorNumber": 5,
            "minFloorNumber": -1
        }
    }
]

twinname = "Eng1"

client.update_digital_twin(twinname, patch)

getTwin(client, twinname)