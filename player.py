#!/usr/bin/env python3
import json
import argparse
import webbrowser
import paho.mqtt.client as mqtt
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
    except Exception as e:
        print(f"[WARN] bad payload: {e} -> {msg.payload[:80]}")
        return

    action = data.get("action", "play")
    url = data.get("url")
    playlist = data.get("playlist")
    reason = data.get("reason")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-read-playback-state,user-modify-playback-state"))
    print(f"[CMD] action={action} playlist={playlist} url={url} reason={reason}")
    if action == "play" and url:
        sp.start_playback(context_uri=url) 
    elif action == "pause":
        print("[INFO] Pause command received (nothing to do in browser mode).")

def main():
    parser = argparse.ArgumentParser(description="Music command subscriber → open browser")
    parser.add_argument("--broker", default="localhost", help="MQTT broker host")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--topic", default="music/cmd", help="MQTT topic to subscribe")
    args = parser.parse_args()

    client = mqtt.Client(client_id="music_cmd_sub")
    client.on_message = on_message
    client.connect(args.broker, args.port, keepalive=60)
    client.subscribe(args.topic, qos=0)
    print(f"[INFO] Subscribed to mqtt://{args.broker}:{args.port}/{args.topic}")
    client.loop_forever()

if __name__ == "__main__":
    main()
