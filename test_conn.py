
import requests
import sys

try:
    print("Testing connection to http://127.0.0.1:8000/api/chat...")
    response = requests.post("http://127.0.0.1:8000/api/chat", json={"question": "hello"})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
