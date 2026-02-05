import requests
import json
import time

base_url = "http://127.0.0.1:8000"
chat_url = f"{base_url}/api/chat"
token_url = f"{base_url}/auth/token"

headers = {"Content-Type": "application/json"}
token_header = {}

def login():
    print("--- Logging in... ---")
    payload = {
        "username": "student",
        "password": "student123"
    }
    # OAuth2 form request usually requires form data, not JSON
    try:
        response = requests.post(token_url, data=payload) # Form data
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"Login Successful. Token: {token[:10]}...")
            return token
        else:
            print(f"Login Failed: {response.text}")
            return None
    except Exception as e:
        print(f"Login Error: {e}")
        return None

def test_query(question, label, token):
    if not token:
        print("Skipping test due to missing token.")
        return

    print(f"\n--- Testing {label} ---")
    print(f"Question: {question}")
    
    current_headers = headers.copy()
    current_headers["Authorization"] = f"Bearer {token}"
    
    payload = {"question": question}
    try:
        start = time.time()
        response = requests.post(chat_url, json=payload, headers=current_headers)
        end = time.time()
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data.get('answer')}")
            print(f"Sources: {data.get('sources')}")
        else:
            print(f"Error: {response.text}")
        print(f"Time taken: {end - start:.2f}s")
    except Exception as e:
        print(f"Request failed: {e}")

# Main execution
token = login()
if token:
    # 1. General Chat
    test_query("Hello! Who are you and what do you do?", "General Chat", token)

    # 2. Academic Chat
    test_query("What is the detailed syllabus for Unit 1?", "Academic Chat", token)

    # 3. Mode Switch Attempt
    test_query("Tell me a fun fact about AI.", "General Chat (Fun Fact)", token)
