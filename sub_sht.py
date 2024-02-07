import random
import mylib

mqtt_broker = '133.11.95.82'
mqtt_port = 18884
mqtt_client_id = f'python-mqtt-{random.randint(0,100)}'
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

mqtt_client = mylib.connect_mqtt(mqtt_client_id, mqtt_broker, mqtt_port)

if __name__ == '__main__':
    for name in sensorNames:
        topic = name+'/01/sht31'
        mylib.set_on_message_sht_sensor(mqtt_client, topic)
        mqtt_client.subscribe(topic)
    mqtt_client.loop_forever()