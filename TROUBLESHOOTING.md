# MoodMusicAssistant Troubleshooting Guide

## Quick Fix - Restart Everything

If your system stopped working after closing a command prompt, try this:

### Option 1: Use the Startup Script (Recommended)
```bash
# Windows
start_mood_music.bat

# Or Python version
python start_mood_music.py
```

### Option 2: Manual Restart
1. **Start MQTT Broker** (if not running):
   ```bash
   mosquitto -v
   ```

2. **Start Node-RED** (if using):
   ```bash
   node-red -p 1880 -s nodered_flow.json
   ```

3. **Start Mood Camera**:
   ```bash
   python mood_cam.py
   ```

4. **Start Music Subscriber**:
   ```bash
   python music_cmd_sub.py
   ```

## Common Issues and Solutions

### 1. "Module not found" errors
**Problem**: Python can't find required modules
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### 2. MQTT Connection Failed
**Problem**: `Connection refused` or `Connection failed`
**Solutions**:
- Install MQTT broker (Mosquitto):
  - Windows: Download from https://mosquitto.org/download/
  - Linux: `sudo apt-get install mosquitto mosquitto-clients`
  - macOS: `brew install mosquitto`
- Start MQTT broker: `mosquitto -v`

### 3. Camera not working
**Problem**: "Cannot open camera" error
**Solutions**:
- Check if camera is being used by another application
- Try different camera index: `python mood_cam.py --camera 1`
- On Windows, make sure camera permissions are enabled

### 4. WebSocket connection failed
**Problem**: Browser shows "Disconnected from Mood Assistant"
**Solutions**:
- Make sure `music_cmd_sub.py` is running
- Check if port 8765 is available
- Try refreshing the browser page

### 5. No music playing
**Problem**: Mood detected but no music plays
**Solutions**:
- Check if Node-RED is running and flow is deployed
- Verify MQTT topics are correct (`ai/mood` and `music/cmd`)
- Check browser console for JavaScript errors

### 6. Spotify authentication issues
**Problem**: Spotify API errors
**Solutions**:
- Set up Spotify app credentials
- Install spotipy: `pip install spotipy`
- Configure Spotify OAuth (see Spotify Developer Console)

## Service Dependencies

Your system requires these services to run in order:

1. **MQTT Broker** (Mosquitto) - Port 1883
2. **Node-RED** (optional) - Port 1880
3. **Mood Camera** (`mood_cam.py`) - Publishes to `ai/mood`
4. **Music Subscriber** (`music_cmd_sub.py`) - WebSocket server on port 8765

## Port Usage

- **1883**: MQTT Broker
- **1880**: Node-RED (if used)
- **8765**: WebSocket server
- **8000**: Web server (for player.html)

## Testing Individual Components

### Test MQTT Connection
```python
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("localhost", 1883, 60)
print("MQTT connected!")
client.disconnect()
```

### Test Mood Detection
```bash
python mood_cam.py --interval 1.0
```

### Test Music Commands
```bash
python test_publish.py
```

## Logs and Debugging

- **Mood Camera**: Shows emotion detection results in console
- **Music Subscriber**: Shows MQTT messages and WebSocket connections
- **Browser Console**: Check for JavaScript errors (F12)
- **Node-RED**: Check debug output in the flow

## System Requirements

- Python 3.7+
- Webcam
- MQTT Broker (Mosquitto)
- Node-RED (optional)
- Modern web browser with WebSocket support

## Still Having Issues?

1. Check all services are running
2. Verify port availability
3. Check firewall settings
4. Review error messages in console
5. Try restarting all services in order
