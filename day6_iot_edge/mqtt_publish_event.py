"""Day 6 demo: publish AI vision events to MQTT."""
import json
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"  # Replace with broker IP, e.g. Raspberry Pi IP
PORT = 1883
TOPIC = "vision/cam01/events"

client = mqtt.Client(client_id="vision-publisher-cam01")
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
