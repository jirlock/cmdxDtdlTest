import struct
from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient
from paho.mqtt import client as mqttClient

def convertTopic2Id(topic):
    topic = topic[:17]
    return topic.replace(":", "")

def connect_mqtt(client_id, broker, port) -> mqttClient:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqttClient.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def set_on_message_ir_sensor(azure_client, mqtt_client, topic):

    def send_patch(twinname, compname, time, tmp, arr):
        patch = [
            {
                "op": "add",
                "path": "/time",
                "value": time
            },
            {
                "op": "add",
                "path": "/temperature",
                "value": tmp
            },
            {
                "op": "add",
                "path": "/arrTemperature",
                "value": arr
            }
        ]
        azure_client.update_component(twinname, compname, patch)

    def on_message_irsensor(client, userdata, msg):
        top = msg.topic
        time = struct.unpack('>q', msg.payload[:8])[0]
        temp = struct.unpack('>f', msg.payload[12:16])[0]
        arrTemp = [struct.unpack('>f', msg.payload[16+i*4:16+(i+1)*4])[0] for i in range(64)]

        print(convertTopic2Id(top))
        send_patch(convertTopic2Id(top), 'IRSensorComp', time, temp, arrTemp)
    
    mqtt_client.message_callback_add(topic, on_message_irsensor)

    


