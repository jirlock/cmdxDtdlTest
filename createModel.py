from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient

url = "https://recTest.api.jpe.digitaltwins.azure.net"

credential = DefaultAzureCredential()
client = DigitalTwinsClient(url, credential)

new_comp = {
    "@id": "dtmi:mycomp:LR15_Temperature_Sensor;1",
    "@type": "Interface",
    "@context": "dtmi:dtdl:context;3",
    "contents": [
        {
            "@type": "Property",
            "name": "time",
            "schema": "long"
        },
        {
            "@type": "Property",
            "name": "temperature",
            "schema": "float"
        },
        {
            "@type": "Property",
            "name": "arrTemperature",
            "schema": {
                "@type": "Array",
                "elementSchema": "float"
            }
        }
    ]
}

new_model = {
    "@id": "dtmi:mymodel:LR15_Temperature_Sensor;1",
    "@type": "Interface",
    "@context": "dtmi:dtdl:context;3",
    "extends": "dtmi:org:brickschema:schema:Brick:Temperature_Sensor;1",
    "contents": [
        {
            "@type": "Component",
            "name": "IRSensorComp",
            "schema": "dtmi:mycomp:LR15_Temperature_Sensor;1"
        }
    ]
}

#client.delete_model("dtmi:mymodel:LR15_Temperature_Sensor;1")
#client.delete_model("dtmi:mycomp:LR15_Temperature_Sensor;1")
model = client.create_models([new_comp, new_model])
print(model)
