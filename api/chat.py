from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from pathlib import Path
from jose import JWTError, jwt

# Add root directory to sys.path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        # Lazy imports inside method to prevent import-time crashes
        try:
            from backend.rag_engine import RAGService
            from backend.auth import SECRET_KEY, ALGORITHM, load_users
            rag_service = RAGService()
        except Exception as e:
            self.send_error_response(500, f"Initialization error: {str(e)}")
            return

        # Auth Check
        user = self.get_current_user(SECRET_KEY, ALGORITHM, load_users)
        if not user:
            self.send_error_response(401, "Not authorized")
            return
            
        if user.get('role') != 'student':
            self.send_error_response(403, "Student access required")
            return

        try:
            data = json.loads(body)
            question = data.get('question')
            if not question:
                self.send_error_response(400, "Question is required")
                return

            answer, sources = rag_service.answer_question(question)
            self.send_success_response({
                "answer": answer,
                "sources": sources
            })
            
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
        except Exception as e:
            self.send_error_response(500, str(e))

    def get_current_user(self, SECRET_KEY, ALGORITHM, load_users):
        auth_header = self.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                users = load_users()
                return users.get(username)
        except:
            return None
        return None

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
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
