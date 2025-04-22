import paho.mqtt.client as mqtt
import json
import time
import datetime
import random

# MQTT Broker details (EMQX public broker)
BROKER = "broker.emqx.io"
PORT = 1883  # Use 8883 for SSL/TLS if needed

TOPIC = "/measurements/heartrate"
# Generate dynamic values
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
random_heart_rate = random.randint(45, 95)

# JSON message to publish
message = {
    "deviceId": "123456789",
    "measurementTime": current_time,
    "heartRate": random_heart_rate
}


# Convert dictionary to JSON string
payload = json.dumps(message)

# Callback when the client successfully connects
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a message is successfully published
def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully!")

# Create MQTT client
client = mqtt.Client()

# Assign callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the EMQX broker
client.connect(BROKER, PORT, 60)

# Start a background network loop
client.loop_start()

# Wait for connection before publishing
time.sleep(2)

# Publish message
result = client.publish(TOPIC, payload)

# Check if publish was successful
status = result.rc
if status == 0:
    print(f"Published: {payload} to {TOPIC}")
else:
    print("Failed to send message")

# Stop the loop and disconnect
client.loop_stop()
client.disconnect()
