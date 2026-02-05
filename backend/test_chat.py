
import requests
import time

base_url = "http://127.0.0.1:8000"
auth_url = f"{base_url}/api/auth/token" # Wait, main.py has /auth/token included from router
token_url = f"{base_url}/auth/token"
chat_url = f"{base_url}/api/chat"

print("Logging in...")
payload = {"username": "student", "password": "student123"}
try:
    resp = requests.post(token_url, data=payload, timeout=5)
    print(f"Login status: {resp.status_code}")
    if resp.status_code == 200:
        token = resp.json()["access_token"]
        print(f"Token: {token[:10]}...")
        
        print("Sending chat request...")
        headers = {"Authorization": f"Bearer {token}"}
        chat_payload = {"question": "hi"}
        try:
            chat_resp = requests.post(chat_url, json=chat_payload, headers=headers, timeout=10)
            print(f"Chat status: {chat_resp.status_code}")
            try:
                print(chat_resp.json())
            except: 
                print(chat_resp.text.encode('utf-8', errors='ignore'))
        except requests.exceptions.Timeout:
            print("Chat request timed out!")
        except Exception as e:
            print(f"Chat error: {e}")
    else:
        print(f"Login failed: {resp.text}")
except Exception as e:
    print(f"Login error: {e}")
