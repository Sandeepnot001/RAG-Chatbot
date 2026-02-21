from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import shutil
import cgi
from pathlib import Path
from jose import JWTError, jwt

# Add root directory to sys.path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

try:
    from backend.rag_engine import RAGService
    from backend.auth import SECRET_KEY, ALGORITHM, load_users
    rag_service = RAGService()
except ImportError:
    pass

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Auth Check
        user = self.get_current_user()
        if not user or user.get('role') != 'admin':
            self.send_error_response(403, "Admin access required")
            return

        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            if 'file' not in form or 'department' not in form or 'semester' not in form:
                self.send_error_response(400, "Missing required form fields")
                return

            file_item = form['file']
            department = form['department'].value
            semester = form['semester'].value

            if not file_item.filename:
                self.send_error_response(400, "No file uploaded")
                return

            os.makedirs("data/tmp", exist_ok=True)
            temp_path = f"data/tmp/{file_item.filename}"
            with open(temp_path, "wb") as f:
                f.write(file_item.file.read())

            metadata = {
                "source": file_item.filename,
                "department": department,
                "semester": semester
            }
            
            success = rag_service.process_document(temp_path, metadata)
            
            if success:
                summary = rag_service.generate_summary(temp_path)
                self.send_success_response({
                    "message": f"Successfully uploaded {file_item.filename} for {department} - {semester}",
                    "summary": summary
                })
            else:
                self.send_error_response(500, "Failed to process document")
                
        except Exception as e:
            self.send_error_response(500, str(e))

    def get_current_user(self):
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
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
