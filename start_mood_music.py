#!/usr/bin/env python3
"""
MoodMusicAssistant Startup Script
This script starts all required services for the MoodMusicAssistant project.
"""

import subprocess
import sys
import time
import os
import webbrowser
from pathlib import Path

def run_command(cmd, shell=True, check=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=shell, check=check, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_python_dependencies():
    """Check if all Python dependencies are installed"""
    print("[INFO] Checking Python dependencies...")
    
    required_packages = ['opencv-python', 'fer', 'numpy', 'paho-mqtt', 'spotipy', 'websockets']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"[ERROR] Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        success, stdout, stderr = run_command(f"pip install --user {' '.join(missing_packages)}")
        if not success:
            print(f"[ERROR] Failed to install packages: {stderr}")
            return False
        print("[SUCCESS] All packages installed successfully!")
    else:
        print("[SUCCESS] All Python dependencies are available!")
    
    return True

def check_mqtt_broker():
    """Check if MQTT broker is running"""
    print("[INFO] Checking MQTT broker...")
    
    try:
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        client.connect('localhost', 1883, 60)
        client.disconnect()
        print("[SUCCESS] MQTT broker is running!")
        return True
    except Exception as e:
        print(f"[ERROR] MQTT broker not running: {e}")
        print("Please start MQTT broker (Mosquitto) manually or install it:")
        print("Windows: Download from https://mosquitto.org/download/")
        print("Linux: sudo apt-get install mosquitto mosquitto-clients")
        print("macOS: brew install mosquitto")
        return False

def start_services():
    """Start all required services"""
    print("[INFO] Starting MoodMusicAssistant services...")
    
    # Start mood camera
    print("[INFO] Starting mood camera...")
    mood_cam_process = subprocess.Popen([sys.executable, "mood_cam.py"], 
                                       creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    
    # Start music command subscriber
    print("[INFO] Starting music command subscriber...")
    music_sub_process = subprocess.Popen([sys.executable, "music_cmd_sub.py"], 
                                        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    
    # Wait a moment for services to start
    time.sleep(3)
    
    # Open web browser
    print("[INFO] Opening web player...")
    webbrowser.open("http://localhost:8000/player.html")
    
    return mood_cam_process, music_sub_process

def main():
    print("=" * 50)
    print("    MoodMusicAssistant Startup Script")
    print("=" * 50)
    print()
    
    # Check if we're in the right directory
    if not Path("mood_cam.py").exists():
        print("[ERROR] Please run this script from the MoodMusicAssistant directory")
        return 1
    
    # Check Python dependencies
    if not check_python_dependencies():
        return 1
    
    # Check MQTT broker
    if not check_mqtt_broker():
        print("\n[WARNING] Please start MQTT broker and run this script again")
        return 1
    
    # Start services
    try:
        mood_cam_process, music_sub_process = start_services()
        
        print("\n" + "=" * 50)
        print("    All services started successfully!")
        print("=" * 50)
        print()
        print("Services running:")
        print("- MQTT Broker (port 1883)")
        print("- Mood Camera (emotion detection)")
        print("- Music Command Subscriber (WebSocket + Browser)")
        print()
        print("The web player should open automatically in your browser.")
        print("If not, manually open: http://localhost:8000/player.html")
        print()
        print("Press Ctrl+C to stop all services...")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[INFO] Stopping services...")
            mood_cam_process.terminate()
            music_sub_process.terminate()
            print("[SUCCESS] All services stopped!")
            
    except Exception as e:
        print(f"[ERROR] Error starting services: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
