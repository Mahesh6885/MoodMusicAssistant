#!/usr/bin/env python3
"""
Simple mood camera with better error handling
"""

import cv2
import time
import json
import paho.mqtt.client as mqtt
from fer.fer import FER
import numpy as np

# Emotion mapping
EMO_MAP = {
    "happy": "happy",
    "surprise": "happy", 
    "sad": "sad",
    "angry": "angry",
    "disgust": "angry",
    "fear": "stressed",
    "neutral": "relaxed"
}

def map_emotion(emo):
    if emo is None:
        return "relaxed"
    return EMO_MAP.get(emo.lower(), "relaxed")

def main():
    print("=" * 50)
    print("    Simple Mood Camera")
    print("=" * 50)
    
    # Initialize MQTT
    client = mqtt.Client(client_id="simple_mood_cam")
    client.connect("localhost", 1884, 60)
    client.loop_start()
    
    # Initialize camera
    print("[INFO] Initializing camera...")
    cap = cv2.VideoCapture(0)
    
    # Try different camera indices if 0 doesn't work
    if not cap.isOpened():
        print("[WARN] Camera 0 not available, trying camera 1...")
        cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("[ERROR] Cannot open any camera!")
        return
    
    print("[SUCCESS] Camera initialized!")
    
    # Initialize emotion detector
    print("[INFO] Loading emotion detector...")
    detector = FER()
    print("[SUCCESS] Emotion detector ready!")
    
    print("\n[INFO] Camera window will open. Press 'q' to quit.")
    print("[INFO] Make different facial expressions to test mood detection!")
    
    last_mood = None
    last_send_time = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[WARN] Failed to read frame, retrying...")
                time.sleep(0.1)
                continue
            
            # Convert to RGB for FER
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect emotion
            result = detector.top_emotion(rgb)
            if result and result[0] is not None:
                label, score = result
                mood = map_emotion(label)
            else:
                mood = "relaxed"
                score = 0.0
            
            # Display mood on frame
            cv2.putText(frame, f"Mood: {mood} ({score:.2f})", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show frame
            cv2.imshow("Mood Detection - Press 'q' to quit", frame)
            
            # Send mood data if it changed or every 3 seconds
            now = time.time()
            if (mood != last_mood or now - last_send_time > 3.0):
                mood_data = {
                    "playlist": mood,
                    "url": f"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "action": "play"
                }
                
                client.publish("ai/mood", json.dumps(mood_data))
                print(f"[PUB] mood={mood} (score={score:.2f})")
                
                last_mood = mood
                last_send_time = now
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n[INFO] Stopping...")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        client.loop_stop()
        client.disconnect()
        print("[SUCCESS] Camera stopped!")

if __name__ == "__main__":
    main()
