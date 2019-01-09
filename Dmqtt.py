import ipfsapi
import json
import os
import paho.mqtt.client as mqtt
### Configuration
Cpath = os.path.dirname(os.path.realpath(__file__))
with open(Cpath+'/config.json') as f:
    Jconfig = json.load(f)
IPFS_IP = Jconfig['IPFS_IP']
IPFS_PORT = Jconfig['IPFS_PORT']
api = ipfsapi.connect(IPFS_IP,IPFS_PORT)

TEST = "test"
PIN_ADD = "pin_add"

def on_connect(client, userdata,flags_dict, rc):
    client.subscribe(TEST)
    client.subscribe(PIN_ADD)

def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    if msg.topic==TEST:
        print(str(msg.payload))
    if msg.topic==PIN_ADD:
        api.pin_add(str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 0)
client.loop_forever()
