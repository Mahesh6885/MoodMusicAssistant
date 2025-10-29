@echo off
echo ========================================
echo    MoodMusicAssistant Startup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if Node-RED is installed
node-red --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Node-RED not found. Please install Node-RED:
    echo npm install -g node-red
    echo.
)

REM Install Python dependencies
echo [1/5] Installing Python dependencies...
pip install --user -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

REM Start MQTT Broker (Mosquitto)
echo [2/5] Starting MQTT Broker...
start "MQTT Broker" cmd /k "echo Starting MQTT Broker... && mosquitto -v"
timeout /t 3 /nobreak >nul

REM Check if MQTT broker started successfully
echo Testing MQTT connection...
python -c "import paho.mqtt.client as mqtt; client = mqtt.Client(); client.connect('localhost', 1883, 60); print('MQTT Broker is running!'); client.disconnect()" 2>nul
if errorlevel 1 (
    echo WARNING: MQTT Broker might not be running. Please install Mosquitto:
    echo Download from: https://mosquitto.org/download/
    echo.
)

REM Start Node-RED
echo [3/5] Starting Node-RED...
start "Node-RED" cmd /k "echo Starting Node-RED... && node-red -p 1880 -s nodered_flow.json"
timeout /t 5 /nobreak >nul

REM Start Mood Camera
echo [4/5] Starting Mood Camera...
start "Mood Camera" cmd /k "echo Starting Mood Camera... && python mood_cam.py"

REM Start Music Command Subscriber
echo [5/5] Starting Music Command Subscriber...
start "Music Command Subscriber" cmd /k "echo Starting Music Command Subscriber... && python music_cmd_sub.py"

echo.
echo ========================================
echo    All services started successfully!
echo ========================================
echo.
echo Services running:
echo - MQTT Broker (port 1883)
echo - Node-RED (http://localhost:1880)
echo - Mood Camera (emotion detection)
echo - Music Command Subscriber (WebSocket + Browser)
echo.
echo The web player should open automatically in your browser.
echo If not, manually open: http://localhost:8000/player.html
echo.
echo Press any key to close this window...
pause >nul
