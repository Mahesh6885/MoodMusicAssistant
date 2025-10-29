import json
import time
import asyncio
import websockets
import threading
import webbrowser
import paho.mqtt.client as mqtt

# Track last mood, time, consecutive count, and first mood flag
last_mood = None
last_time = 0
mood_counter = 0
first_mood_received = False
connected_clients = set()

# ---------- WebSocket Handler ----------
async def websocket_handler(websocket):
    connected_clients.add(websocket)
    try:
        async for _ in websocket:
            pass  # We don't expect messages back
    finally:
        connected_clients.remove(websocket)

async def websocket_server():
    async with websockets.serve(websocket_handler, "localhost", 8765):
        await asyncio.Future()  # Run forever

def websocket_thread():
    asyncio.run(websocket_server())

# ---------- MQTT Handler ----------
def on_message(client, userdata, msg):
    global last_mood, last_time, mood_counter, first_mood_received

    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        action = data.get("action")
        playlist = data.get("playlist")
        url = data.get("url")
        mood = playlist

        now = time.time()

        # First mood logic: play immediately
        if not first_mood_received:
            first_mood_received = True
            last_mood = mood
            last_time = now
            mood_counter = 1
            send_message_to_browser(mood, url, action)
            print(f"[FIRST] Mood '{mood}' detected, playing immediately.")
            return

        # Count consecutive same moods
        if mood == last_mood:
            mood_counter += 1
        else:
            mood_counter = 1

        last_mood = mood

        # Only proceed if mood detected 5 times consecutively
        if mood_counter < 5:
            print(f"[WAIT] Mood '{mood}' detected {mood_counter}/5 times")
            return

        # Avoid refreshing if same mood within 30 sec
        if (now - last_time) < 30:
            print(f"[SKIP] Mood '{mood}' already playing recently, no refresh.")
            return

        last_time = now

        # Send update to connected WebSocket clients
        send_message_to_browser(mood, url, action)

    except Exception as e:
        print(f"[ERROR] Failed to process MQTT message: {e}")

def send_message_to_browser(mood, url, action):
    if connected_clients:
        message = json.dumps({"action": action, "url": url, "mood": mood})
        asyncio.run(send_to_clients(message))
        print(f"[CMD] Sent to browser → {message}")
    else:
        print("[WARN] No browser connected yet.")

async def send_to_clients(message):
    if connected_clients:
        await asyncio.gather(*[ws.send(message) for ws in connected_clients])

# ---------- Main ----------
def main():
    # Start WebSocket server in background
    threading.Thread(target=websocket_thread, daemon=True).start()
    time.sleep(1)  # Give WebSocket time to start

    # Open browser only once
    webbrowser.open("http://localhost:8000/player.html", new=1)

    # Setup MQTT
    client = mqtt.Client(client_id="music_cmd_sub")
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("music/cmd")
    print("[INFO] Subscribed to mqtt://localhost:1883/music/cmd")

    client.loop_forever()

if __name__ == "__main__":
    main()
