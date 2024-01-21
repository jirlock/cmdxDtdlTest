from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient

url = "https://recTest.api.jpe.digitaltwins.azure.net"

credential = DefaultAzureCredential()
client = DigitalTwinsClient(url, credential)

new_comp = {
    "@id": "dtmi:mycomp:LR15_Temperature_Sensor;1",
    "@type": "Interface",
    "@context": "dtmi:dtdl:context;3",
    #"extends": "dtmi:org:brickschema:schema:Brick:Temperature_Sensor;1",
    "contents": [
        {
            "@type": "Property",
            "name": "LR15_IRSensor_Telemetries",
            "schema": {
                "@type": "Object",
                "fields": [
                    {
                        "name": "time",
                        "schema": "long"
                    },
                    {
                        "name": "temp",
                        "schema": "float"
                    },
                    {
                        "name": "arrTemp",
                        "schema": {
                            "@type": "Array",
                            "elementSchema": "float"
                        }
                    }
                ]
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

tmp_model = {
  "@context": "dtmi:dtdl:context;3",
  "@id": "dtmi:com:example:Thermostat;1",
  "@type": "Interface",
  "displayName": "Thermostat",
  "contents": [
    {
      "@type": "Telemetry",
      "name": "temp",
      "schema": "double"
    },
    {
      "@type": "Property",
      "name": "setPointTemp",
      "writable": True,
      "schema": "double"
    }
  ]
}

model = client.create_models([new_model])
print(model)
