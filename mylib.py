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

#Parser
def parse_ir_sensor(msg):
    topic = msg.topic
    time = struct.unpack('>q', msg.payload[:8])[0]
    temperature = struct.unpack('>f', msg.payload[12:16])[0]
    arrayTemperature = [struct.unpack('>f', msg.payload[16+i*4:16+(i+1)*4])[0] for i in range(64)]
    return topic, time, temperature, arrayTemperature

def parse_ill_sensor(msg):
    topic = msg.topic
    time = struct.unpack('>q', msg.payload[:8])[0]
    illumination = struct.unpack('>H', msg.payload[12:16])[0]
    return topic, time, illumination

def parse_sht_sensor(msg):
    topic = msg.topic
    time = struct.unpack('>q', msg.payload[:8])[0]
    temperature = struct.unpack('>f', msg.payload[12:16])[0]
    humidity = struct.unpack('>f', msg.payload[16:20])[0]
    return topic, time, temperature, humidity

#Callback Function
def set_on_message_ir_sensor_azure(azure_client, mqtt_client, topic):
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
        topic, time, temperature, arrayTemperature = parse_ir_sensor(msg)
        print(convertTopic2Id(topic))
        send_patch(convertTopic2Id(topic), 'IRSensorComp', time, temperature, arrayTemperature)
    mqtt_client.message_callback_add(topic, on_message_irsensor)

def set_on_message_ir_sensor_print(mqtt_client, topic):
    def on_message(client, userdata, msg):
        topic, time, temperature, arrayTemperature = parse_ir_sensor(msg)
        print(convertTopic2Id(topic))
        print(time)
        print(temperature)
        print(arrayTemperature)
    mqtt_client.message_callback_add(topic, on_message)

def set_on_message_ill_sensor_print(mqtt_client, topic):
    def on_message_ill_sensor(client, userdata, msg):
        topic, time, illumination = parse_ill_sensor(msg)
        print(convertTopic2Id(topic))
        print(time)
        print(illumination)
    mqtt_client.message_callback_add(topic, on_message_ill_sensor)

def set_on_message_sht_sensor_print(mqtt_client, topic):
    def on_message_sht_sensor(client, userdata, msg):
        topic, time, temperature, humidity = parse_sht_sensor(msg)
        print(convertTopic2Id(topic))
        print(time)
        print(temperature)
        print(humidity)
    mqtt_client.message_callback_add(topic, on_message_sht_sensor)

def set_on_message_ir_sensor_graphdb(mqtt_client, topic):
    def on_message(client, userdata, msg):
        topic, time, temperature, arrayTemperature = parse_ir_sensor(msg)



