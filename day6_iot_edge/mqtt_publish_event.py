"""Day 6 demo: publish AI vision events to MQTT."""
import json
import time
import random
import paho.mqtt.client as mqtt

BROKER = "localhost"  # Replace with broker IP, e.g. Raspberry Pi IP
#BROKER = "test.mosquitto.org"  # Public test broker for demo
PORT = 1883
TOPIC = "vision/cam01/events"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code", rc)

def on_publish(client, userdata, mid):
    print("Message published with mid:", mid)

client = mqtt.Client(client_id="vision-publisher-cam01")
client.on_connect = on_connect
client.on_publish = on_publish      

client.connect(BROKER, PORT, keepalive=60)

for i in range(5):
    event = {
        "camera_id": "cam01",
        "device": "raspberry-pi-gateway",
        "event_type": "object_detected",
        "label": "person",
        "confidence": 0.85,
        "timestamp": time.time(),
    }
    client.publish(TOPIC, json.dumps(event), qos=1)
    print("Published:", event)
    time.sleep(2)

client.disconnect()
