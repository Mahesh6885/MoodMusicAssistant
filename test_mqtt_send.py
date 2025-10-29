import paho.mqtt.client as mqtt
import json
import time

client = mqtt.Client("test_pub")
client.connect("localhost", 1883, 60)

while True:
    payload = json.dumps({"playlist":"happy","url":"http://example.com","action":"play"})
    client.publish("ai/mood", payload)
    print("Sent:", payload)
    time.sleep(5)
