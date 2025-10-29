#!/usr/bin/env python3
import cv2
import time
import json
import argparse
import numpy as np
from fer.fer import FER
import paho.mqtt.client as mqtt

EMO_MAP = {
    "happy": "happy",
    "surprise": "happy",
    "sad": "sad",
    "angry": "angry",
    "disgust": "angry",
    "fear": "stressed",
    "neutral": "relaxed"
}

def map_emotion(emo: str) -> str:
    return EMO_MAP.get(emo.lower(), "relaxed")

def main():
    parser = argparse.ArgumentParser(description="Webcam emotion → MQTT publisher")
    parser.add_argument("--broker", default="localhost", help="MQTT broker host")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--topic", default="ai/mood", help="MQTT topic to publish mood")
    parser.add_argument("--interval", type=float, default=2.0, help="Seconds between inferences")
    parser.add_argument("--camera", type=int, default=0, help="Webcam index")
    args = parser.parse_args()

    client = mqtt.Client(client_id="mood_cam_pub")
    client.connect(args.broker, args.port, keepalive=60)
    client.loop_start()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera. Try a different --camera index.")

    detector = FER()  # Uses a pre-trained CNN (FER2013)

    print(f"[INFO] Publishing moods to mqtt://{args.broker}:{args.port}/{args.topic}")
    last_send = 0.0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("[WARN] Frame grab failed"); time.sleep(0.1); continue

            # FER expects RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Get the top emotion (label, score)
            label, score = detector.top_emotion(rgb) or (None, 0)
            if label is None:
                mood = "relaxed"
            else:
                mood = map_emotion(label)

            now = time.time()
            if now - last_send >= args.interval:
                payload = mood  # keep it simple for Node-RED function
                client.publish(args.topic, payload, qos=0, retain=False)
                if score is not None:
                    print(f"[PUB] mood={mood} (raw={label}, score={score:.2f})")
                else:
                    print(f"[PUB] mood={mood} (raw={label}, score=None)")
                last_send = now

            # Optional preview window (press q to quit)
            cv2.putText(frame, f"Mood: {mood}", (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            cv2.imshow("Mood-Aware (press q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
