from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient
import pandas as pd
import numpy as np
import mylib

def parseList(l):
    level = str(int(l[0]))
    id = str(l[1])
    if id == "nan":
        id = ''
    name = l[2]
    modelpath = ''
    try:
        modelpath = modeldict[l[3]]
    except:
        modelpath = 'dtmi:org:w3id:rec:Room;1'
    digital_twin_id = level + '_' + id + '_' + name
    modeltype = l[4]

    return level, id, name, modelpath, modeltype, digital_twin_id

url = "https://recTest.api.jpe.digitaltwins.azure.net"

credential = DefaultAzureCredential()
client = DigitalTwinsClient(url, credential)

twinlist_filepath = "Eng10RoomList.xlsx"
twinlist_df = pd.read_excel(twinlist_filepath)
twinlist_np = twinlist_df.to_numpy()

modeldict = {
    'Laboratory': 'dtmi:org:w3id:rec:Laboratory;1',
    'Stairwell': 'dtmi:org:w3id:rec:Stairwell;1',
    'ElevatorRoom': 'dtmi:org:w3id:rec:ElevatorRoom;1',
    'Storage': 'dtmi:org:w3id:rec:Storage;1',
    'OutdoorSpace': 'dtmi:org:w3id:rec:OutdoorSpace;1',
    'ConferenceRoom': 'dtmi:org:w3id:rec:ConferenceRoom;1',
    'Bathroom': "dtmi:org:w3id:rec:Bathroom;1",
    'SafetyShower': 'dtmi:org:brickschema:schema:Brick:Safety_Shower;1',
    'Office': 'dtmi:org:w3id:rec:Office;1',
    'MainEntrance': 'dtmi:org:w3id:rec:MainEntrance;1',
    'StorageCabinet': 'dtmi:org:w3id:rec:StorageCabinet;1',
    'Lounge': 'dtmi:org:w3id:rec:Lounge;1'
}

for i in range(len(twinlist_np)):

    level, id, name, modelpath, modeltype, digital_twin_id = parseList(twinlist_np[i])

    temporary_twin = {}

    if modeltype == 'r' or modeltype == 'b':
        temporary_twin = {
            "$metadata": {
                "$model": modelpath
            },
            "$dtId": digital_twin_id,
            "name": name
        }
    else:
        temporary_twin = {
            "$metadata": {
                "$model": modelpath
            },
            "$dtId": digital_twin_id,
            "name": name,
            "area": {"$metadata": {}},
            "capacity": {"$metadata": {}}
        }
    
    print(digital_twin_id)
    created_twin = client.upsert_digital_twin(digital_twin_id, temporary_twin)
    print(created_twin)

    #Relations
    relationship = {}
    if modeltype == 'b':
        pass
    else:
        relationship = {
            "$relationshipId": "rel_" + digital_twin_id,
            "$sourceId": "Eng10_" + level,
            "$relationshipName": "isLocationOf",
            "$targetId": digital_twin_id
        }

        client.upsert_relationship(
            relationship["$sourceId"],
            relationship["$relationshipId"],
            relationship
        )
    

