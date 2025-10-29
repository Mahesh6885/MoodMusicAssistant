import json
import time
import asyncio
import websockets
import threading
import webbrowser
import paho.mqtt.client as mqtt

# Global state
last_mood = None
last_time = 0
mood_counter = 0
first_mood_received = False
connected_clients = set()
ws_loop = None  # asyncio loop for WebSocket

# ---------- WebSocket ----------
async def websocket_handler(websocket):
    connected_clients.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        connected_clients.remove(websocket)

async def websocket_server():
    async with websockets.serve(websocket_handler, "localhost", 8765):
        await asyncio.Future()  # run forever

def websocket_thread():
    global ws_loop
    ws_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(ws_loop)
    ws_loop.run_until_complete(websocket_server())

# ---------- MQTT ----------
def on_message(client, userdata, msg):
    global last_mood, last_time, mood_counter, first_mood_received

    try:
        payload = msg.payload.decode()
        print(f"[MQTT RECEIVED RAW] {payload}")  # Debug

        data = json.loads(payload)
        mood = data.get("playlist", "")
        action = data.get("action", "")
        url = data.get("url", "")

        now = time.time()

        if not first_mood_received:
            first_mood_received = True
            last_mood = mood
            last_time = now
            mood_counter = 1
            send_message_to_browser(mood, url, action)
            print(f"[FIRST] Mood '{mood}' detected, playing immediately.")
            return

        if mood == last_mood:
            mood_counter += 1
        else:
            mood_counter = 1

        last_mood = mood

        if mood_counter < 5:
            print(f"[WAIT] Mood '{mood}' detected {mood_counter}/5 times")
            return

        if (now - last_time) < 30:
            print(f"[SKIP] Mood '{mood}' already playing recently, no refresh.")
            return

        last_time = now
        send_message_to_browser(mood, url, action)

    except Exception as e:
        print(f"[ERROR] Failed to process MQTT message: {e}")

def send_message_to_browser(mood, url, action):
    if connected_clients:
        message = json.dumps({"action": action, "url": url, "mood": mood})
        ws_loop.call_soon_threadsafe(asyncio.create_task, send_to_clients(message))
        print(f"[CMD] Sent to browser → {message}")
    else:
        print("[WARN] No browser connected yet.")

async def send_to_clients(message):
    if connected_clients:
        await asyncio.gather(*[ws.send(message) for ws in connected_clients])

# ---------- Main ----------
def main():
    # Start WebSocket in background
    threading.Thread(target=websocket_thread, daemon=True).start()
    time.sleep(1)

    # Open browser once
    webbrowser.open("http://localhost:8000/player.html", new=1)

    # MQTT setup
    client = mqtt.Client(client_id="music_cmd_sub")
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("ai/mood")
    print("[INFO] Subscribed to mqtt://localhost:1883/ai/mood")

    client.loop_forever()

if __name__ == "__main__":
    main()
