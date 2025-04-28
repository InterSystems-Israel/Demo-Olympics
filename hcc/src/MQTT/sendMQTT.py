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

# Callback when the client successfully connects (MQTT v5 style)
def on_connect(client, userdata, flags, reasonCode, properties):
    if reasonCode == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, reason code {reasonCode}")

# Callback when a message is successfully published (MQTT v5 style)
def on_publish(client, userdata, mid, reasonCode, properties):
    print(f"Message {mid} published successfully with reason code: {reasonCode}")

# Create MQTT client using MQTT v5 callback API
client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311
)

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
if result.rc == 0:
    print(f"Published: {payload} to {TOPIC}")
else:
    print("Failed to send message")

# Stop the loop and disconnect
time.sleep(1)  # Give some time for publish callback to complete
client.loop_stop()
client.disconnect()
