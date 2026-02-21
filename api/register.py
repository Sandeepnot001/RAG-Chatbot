from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from pathlib import Path

# Add the root directory to sys.path so we can import from backend
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

try:
    from backend.auth import load_users, save_users, pwd_context
except ImportError:
    # Fallback if imports fail during deployment or local testing
    pass

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
            username = data.get('username')
            password = data.get('password')
            role = data.get('role')

            if not username or not password or not role:
                self.send_error_response(400, "Missing required fields")
                return

            if role not in ["admin", "student"]:
                self.send_error_response(400, "Invalid role")
                return

            users = load_users()
            if username in users:
                self.send_error_response(400, "Username already registered")
                return

            hashed_password = pwd_context.hash(password)
            new_user = {
                "username": username,
                "role": role,
                "hashed_password": hashed_password
            }
            
            users[username] = new_user
            save_users(users)

            self.send_success_response({"message": "User registered successfully"})
            
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
        except Exception as e:
            self.send_error_response(500, str(e))

    def send_success_response(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"detail": message}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
