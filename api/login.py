from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from datetime import timedelta
from pathlib import Path
from urllib.parse import parse_qs

# Add the root directory to sys.path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            from backend.auth import load_users, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
        except Exception as e:
            self.send_error_response(500, f"Import error: {str(e)}")
            return

        # Determine if it's JSON or Form data
        content_type = self.headers.get('Content-Type', '')
        
        username = None
        password = None

        if 'application/json' in content_type:
            try:
                data = json.loads(body)
                username = data.get('username')
                password = data.get('password')
            except json.JSONDecodeError:
                self.send_error_response(400, "Invalid JSON")
                return
        elif 'application/x-www-form-urlencoded' in content_type:
            params = parse_qs(body)
            username = params.get('username', [None])[0]
            password = params.get('password', [None])[0]
        else:
            self.send_error_response(400, "Unsupported Content-Type")
            return

        if not username or not password:
            self.send_error_response(400, "Missing credentials")
            return

        users = load_users()
        user_dict = users.get(username)
        
        if not user_dict or not verify_password(password, user_dict.get('hashed_password')):
            self.send_error_response(401, "Incorrect username or password")
            return

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username, "role": user_dict.get('role')}, 
            expires_delta=access_token_expires
        )

        self.send_success_response({
            "access_token": access_token,
            "token_type": "bearer",
            "role": user_dict.get('role')
        })

    def send_success_response(self, data):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"detail": message}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
