import ipfsapi
import json
import os
import paho.mqtt.client as mqtt
### Configuration
Cpath = os.path.dirname(os.path.realpath(__file__))
with open(Cpath+'/../../config.json') as f:
    Jconfig = json.load(f)
IPFS_IP = Jconfig['IPFS_IP']
IPFS_PORT = Jconfig['IPFS_PORT']
api = ipfsapi.connect(IPFS_IP,IPFS_PORT)

TEST = "test"
PIN_ADD = "pin_add"
CALL_PEER = "call_peer"

def Publish(target, channel, message):
    client = mqtt.Client()
    client.max_inflight_messages_set(200000)
    client.connect(target, Jconfig['MQTT_PORT'])
    client.loop_start()
    msg_info = client.publish(channel, message, qos=1)
    if msg_info.is_published() == False:
        msg_info.wait_for_publish()
    client.disconnect()

def on_connect(client, userdata,flags_dict, rc):
    client.subscribe(TEST)
    client.subscribe(CALL_PEER)
    client.subscribe(PIN_ADD)

def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    if msg.topic==TEST:
        print(str(msg.payload))
    if msg.topic==CALL_PEER:
        print(str(msg.payload))
        Publish(str(msg.payload),'test','test')
    if msg.topic==PIN_ADD:
        api.pin_add(str(msg.payload))
        print("KEVIN PIN ADD : "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", Jconfig["MQTT_PORT"], 0)
client.loop_forever()
