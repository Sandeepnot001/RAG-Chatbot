from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from pathlib import Path

# Add root directory to sys.path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "ok", 
            "message": "CollegeBot API is healthy",
            "python_version": sys.version
        }).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
