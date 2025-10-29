# MoodMusicAssistant

A real-time mood detection system that plays music based on facial expressions detected from your webcam.

## Features

- **Real-time Mood Detection**: Uses computer vision to detect emotions from your webcam
- **Automatic Music Playback**: Plays different music based on detected mood
- **Web Interface**: Beautiful web player with mood visualization
- **MQTT Communication**: Uses MQTT for real-time communication between components
- **Multiple Moods**: Supports happy, sad, angry, relaxed, and stressed moods

## Quick Start

### Easy Setup (Recommended)

**Windows:**
```bash
# Double-click or run:
start_project.bat
```

This will automatically:
1. Start MQTT broker on port 1884
2. Start web server on port 8000
3. Start music subscriber
4. Start mood camera
5. Open web player in your browser

### Manual Setup

1. **Start MQTT Broker**
   ```bash
   mosquitto -p 1884 -v
   ```

2. **Start Web Server**
   ```bash
   python -m http.server 8000
   ```

3. **Start Music Subscriber**
   ```bash
   python music_cmd_sub.py
   ```

4. **Start Mood Camera**
   ```bash
   python simple_mood_cam.py
   ```

5. **Open Web Player**
   - Go to `http://localhost:8000/player.html`

## Project Structure

```
MoodMusicAssistant/
├── mood_cam.py              # Main mood detection script
├── music_cmd_sub.py         # MQTT subscriber and music controller
├── simple_mood_cam.py       # Simplified mood camera for testing
├── player.html              # Web interface for mood display and music
├── web_server.py            # Simple HTTP server
├── start_project.bat        # Windows batch startup script
├── start_mood_music.py      # Python startup script
├── start_mood_music.bat     # Alternative batch script
├── requirements.txt         # Python dependencies
├── nodered_flow.json        # Node-RED flow configuration
└── README.md               # This file
```

## Requirements

- Python 3.7+
- Webcam
- MQTT Broker (Mosquitto)
- Internet connection (for YouTube music)

## Dependencies

- opencv-python
- fer
- numpy
- paho-mqtt
- spotipy
- websockets

## Usage

1. **Start the system** using `start_project.bat`
2. **Allow camera access** when prompted
3. **Make facial expressions** - smile, frown, look angry, etc.
4. **Watch the web player** - it will show your detected mood and play music
5. **Use test buttons** on the web page to manually test different moods

## Mood Types

- **Happy**: Upbeat, energetic music
- **Sad**: Calm, melancholic music  
- **Angry**: Intense, powerful music
- **Relaxed**: Soft, peaceful music
- **Stressed**: Calming, meditative music

## Troubleshooting

### Camera Issues
- Make sure your webcam is not being used by another application
- Check camera permissions in your system settings

### MQTT Issues
- Ensure Mosquitto is running on port 1884
- Check if port 1884 is available

### Music Not Playing
- Check browser console for errors (F12)
- Ensure you've clicked on the page to enable auto-play
- Use the test buttons on the web page

## License

This project is open source and available under the MIT License.