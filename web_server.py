#!/usr/bin/env python3
"""
Simple HTTP server for the MoodMusicAssistant web player
"""

import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for WebSocket connections
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_web_server():
    """Start the web server in a separate thread"""
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"[INFO] Web server running at http://localhost:{PORT}")
        print(f"[INFO] Serving player.html at http://localhost:{PORT}/player.html")
        httpd.serve_forever()

def main():
    print("=" * 50)
    print("    MoodMusicAssistant Web Server")
    print("=" * 50)
    print()
    
    # Start web server in background thread
    server_thread = threading.Thread(target=start_web_server, daemon=True)
    server_thread.start()
    
    # Wait a moment for server to start
    time.sleep(1)
    
    # Open browser
    print("[INFO] Opening web player...")
    webbrowser.open(f"http://localhost:{PORT}/player.html")
    
    print(f"[SUCCESS] Web server started! Open http://localhost:{PORT}/player.html")
    print("Press Ctrl+C to stop...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Web server stopped!")

if __name__ == "__main__":
    main()
