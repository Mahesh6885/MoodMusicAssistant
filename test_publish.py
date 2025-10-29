import json
import paho.mqtt.client as mqtt

# Connect to MQTT broker
client = mqtt.Client(client_id="test_pub")
client.connect("localhost", 1883, 60)

# Example message to send
message = {
    "playlist": "happy",
    "url": "https://example.com/song.mp3",
    "action": "play"
}

# Publish to the topic ai/mood
client.publish("ai/mood", json.dumps(message))
print("[INFO] Message sent to ai/mood!")

# Disconnect after sending
client.disconnect()
