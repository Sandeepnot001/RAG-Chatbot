
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_login(username, password):
    print(f"Testing login for {username}...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"SUCCESS: Login successful for {username}")
            return token
        else:
            print(f"FAILURE: Login failed for {username}. Status: {response.status_code}, Body: {response.text}")
            return None
    except Exception as e:
        print(f"ERROR: Could not connect to backend. {e}")
        return None

def test_chat(token):
    print("\nTesting Chat Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": "Hello, who are you?"}
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            headers=headers,
            timeout=30 # 30s timeout
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            print(f"SUCCESS: Chat response received in {elapsed:.2f}s")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"FAILURE: Chat failed. Status: {response.status_code}, Body: {response.text}")
            
    except requests.exceptions.Timeout:
        print("FAILURE: Chat request timed out (Backend hang confirmed?)")
    except Exception as e:
        print(f"ERROR: Chat request error. {e}")

def main():
    # 1. Test Admin Login
    admin_token = test_login("admin", "admin123")
    
    # 2. Test Student Login
    student_token = test_login("student", "student123")
    
    if student_token:
        # 3. Test Chat
        test_chat(student_token)

if __name__ == "__main__":
    main()
