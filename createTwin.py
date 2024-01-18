from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient

url = "https://recTest.api.jpe.digitaltwins.azure.net"

credential = DefaultAzureCredential()
client = DigitalTwinsClient(url, credential)

digital_twin_id = "Engineering1"

temporary_twin = {
    "$metadata": {
        "$model": "dtmi:org:w3id:rec:Building;1"
    },
    "$dtId": digital_twin_id,
    "name": "Engineering1",
    "area": {"$metadata":{}},
    "capacity": {"$metadata":{}}
}

created_twin = client.upsert_digital_twin(digital_twin_id, temporary_twin)

print(created_twin)