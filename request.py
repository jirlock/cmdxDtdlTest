from azure.identity import DefaultAzureCredential
from azure.mgmt.digitaltwins import AzureDigitalTwinsManagementClient
from azure.digitaltwins.core import DigitalTwinsClient
import os
import requests
from requests.auth import HTTPBasicAuth

subscriptionId = "af194cdc-dd36-4e0e-aa3c-0827d9d43f61"
resourceGroupName = "cmdx"
resourceName = "15LectureRoom"
#url = "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + resourceGroupName + "/providers/Microsoft.DigitalTwins/digitalTwinsInstances/" + resourceName + "?api-version=2023-01-31"
url = "https://15LectureRoom.api.jpe.digitaltwins.azure.net"

#sub_id = os.getenv("AZURE_SUBSCRIPTION_ID")
#client = AzureDigitalTwinsManagementClient(credential=DefaultAzureCredential(), subscription_id=subscriptionId).digital_twins

credential = DefaultAzureCredential()
client = DigitalTwinsClient(url, credential)

#get_twin = client.get_digital_twin("Seats")
#print (get_twin)

component_name = "Occupied"
patch = [
    {
        "op": "replace",
        "path": "/Occupied",
        "value": 120
    }
]

#client.update_component("Seats", component_name, patch)

client.update_digital_twin("Seats", patch)