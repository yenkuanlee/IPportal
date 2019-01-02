import paho.mqtt.client as mqtt

def on_connect(client, userdata,flags_dict, rc):
    client.subscribe("test")

def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    if msg.topic=='test':
        print(str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 0)
client.loop_forever()
