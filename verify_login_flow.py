
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_login_and_chat():
    print(f"Testing connectivity to {BASE_URL}...")
    
    # 1. Login
    try:
        login_data = {
            "username": "student",
            "password": "student123"
        }
        print("Attempting Login...")
        response = requests.post(f"{BASE_URL}/auth/token", data=login_data)
        
        if response.status_code != 200:
            print(f"Login Failed: {response.status_code} - {response.text}")
            return False
            
        token_data = response.json()
        token = token_data.get("access_token")
        print(f"Login Successful. Token received. Role: {token_data.get('role')}")
        
        # 2. Test Chat (Protected Route)
        print("Attempting Chat Request...")
        headers = {"Authorization": f"Bearer {token}"}
        chat_data = {"question": "Hello"}
        
        chat_response = requests.post(f"{BASE_URL}/api/chat", json=chat_data, headers=headers)
        
        if chat_response.status_code == 200:
            print("Chat Request Successful!")
            print(f"Response: {chat_response.json()}")
            return True
        else:
            print(f"Chat Request Failed: {chat_response.status_code} - {chat_response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("Connection Error: Could not connect to backend. Is it running?")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    if test_login_and_chat():
        print("Verification Passed.")
        sys.exit(0)
    else:
        print("Verification Failed.")
        sys.exit(1)
