@echo off
echo ================================================
echo    MoodMusicAssistant - Starting Project
echo ================================================

echo [1/4] Starting MQTT Broker...
start "MQTT Broker" cmd /k "mosquitto -p 1884 -v"

echo [2/4] Starting Web Server...
start "Web Server" cmd /k "python -m http.server 8000"

echo [3/4] Starting Music Subscriber...
start "Music Subscriber" cmd /k "python music_cmd_sub.py"

echo [4/4] Starting Mood Camera...
start "Mood Camera" cmd /k "python simple_mood_cam.py"

echo.
echo [INFO] All services starting...
echo [INFO] Opening web player in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:8000/player.html

echo.
echo ================================================
echo    Project Started Successfully!
echo ================================================
echo.
echo Services running:
echo - MQTT Broker: localhost:1884
echo - Web Server: http://localhost:8000
echo - Music Subscriber: Listening for mood commands
echo - Mood Camera: Detecting emotions from webcam
echo.
echo Web Player: http://localhost:8000/player.html
echo.
echo Press any key to exit this window...
pause >nul
