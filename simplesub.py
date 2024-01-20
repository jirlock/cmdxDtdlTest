import random
import struct
from paho.mqtt import client as mqtt_client
#import paho.mqtt.subscribe as subscribe

broker = "133.11.95.82"
port = 18884
#topic = '+/+/info'
#topic = '08:3a:f2:23:cc:80/01/array02'
client_id = f'python-mqtt-{random.randint(0, 100)}'
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

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
        print("================================")
        print(int.from_bytes(msg.payload[0:8], byteorder='big'))
        #print(int.from_bytes(msg.payload[8:12], byteorder='big'))
        print(struct.unpack('>i', msg.payload[8:12])[0])
        print(struct.unpack('>f', msg.payload[12:16])[0])
        temps = []
        for i in range(64):
            temps.append(struct.unpack('>f', msg.payload[16+i*4: 16+(i+1)*4])[0])
        print(temps)

    client.subscribe(topic)
    client.on_message = on_message

def on_message_irsensor(client, userdata, msg):
    print('=================================')
    topic = msg.topic
    temps = []
    for i in range(64):
        temps.append(struct.unpack('>f', msg.payload[16+i*4: 16+(i+1)*4])[0])
    print(topic)
    print(temps)

def run():
    client = connect_mqtt()
    for name in sensorNames:
        topic = name + '/01/array02'
        client.message_callback_add(topic , on_message_irsensor)
        client.subscribe(topic)
    client.loop_forever()

if __name__ == '__main__':
    run()

