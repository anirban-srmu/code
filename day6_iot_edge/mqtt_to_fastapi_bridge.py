"""
Day 6 demo: bridge MQTT events to FastAPI server.
"""

import json
import paho.mqtt.client as mqtt
import requests 

#BROKER = "test.mosquitto.org"  # Public test broker for demo
BROKER = "localhost"  # Replace with broker IP, e.g. Raspberry Pi IP
PORT = 1883
TOPIC = "vision/cam01/events"
API_URL = "http://localhost:8000/events"  # FastAPI server URL  

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code", rc)
    client.subscribe(TOPIC) 

def on_message(client, userdata, msg):
    print(f"Received MQTT message on topic {msg.topic}")
    try:
        payload = msg.payload.decode('utf-8')
        event = json.loads(payload)
        print("Parsed event:", event)
        response = requests.post(
            API_URL, 
            json=event,
            timeout=5,
        )
        print("Forwarded to FastAPI:", response.status_code, response.json())
    except Exception as e:
        print("Error processing message:", e)

client = mqtt.Client(client_id="mqtt-to-fastapi-bridge")
client.on_connect = on_connect
client.on_message = on_message      

client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()