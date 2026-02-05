import requests
import sys

try:
    print("Checking backend on http://127.0.0.1:8000/docs...")
    response = requests.get("http://127.0.0.1:8000/docs", timeout=5)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Backend is running and reachable.")
    else:
        print("Backend is reachable but returned non-200.")
except Exception as e:
    print(f"Error connecting to backend: {e}")
