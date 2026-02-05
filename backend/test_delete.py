
import requests
import json
import os
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_delete_flow():
    print("Testing Delete Flow...")
    
    # 1. Login as Admin
    print("1. Logging in as Admin...")
    try:
        response = requests.post(f"{BASE_URL}/auth/token", data={"username": "admin", "password": "admin123"})
        if response.status_code != 200:
            print(f"Login Failed: {response.text}")
            return False
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("Login Successful.")
    except Exception as e:
        print(f"Connection Error: {e}")
        return False
        
    # 2. Upload Dummy File
    print("2. Uploading Dummy Document...")
    dummy_filename = "test_delete_doc.txt"
    with open(dummy_filename, "w") as f:
        f.write("This is a dummy document to test deletion.")
        
    try:
        with open(dummy_filename, "rb") as f:
            files = {"file": (dummy_filename, f, "text/plain")}
            data = {"department": "Computer Science", "semester": "Semester 1"}
            response = requests.post(f"{BASE_URL}/api/upload", files=files, data=data, headers=headers)
            
        if response.status_code == 200:
            print("Upload Successful.")
        else:
            print(f"Upload Failed: {response.text}")
            return False
    except Exception as e:
        print(f"Upload Error: {e}")
        return False
        
    # 3. Verify it exists
    print("3. Verifying Document Exists...")
    response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
    docs = response.json().get("documents", [])
    if not any(d['name'] == dummy_filename for d in docs):
        print("Document not found in list after upload.")
        return False
    print("Document verified in list.")
    
    # 4. Delete it
    print(f"4. Deleting {dummy_filename}...")
    response = requests.delete(f"{BASE_URL}/api/documents/{dummy_filename}", headers=headers)
    if response.status_code == 200:
        print("Delete Request Successful.")
    else:
        print(f"Delete Failed: {response.status_code} - {response.text}")
        return False
        
    # 5. Verify it is gone
    print("5. Verifying Document is Gone...")
    response = requests.get(f"{BASE_URL}/api/documents", headers=headers)
    docs = response.json().get("documents", [])
    if any(d['name'] == dummy_filename for d in docs):
        print("Document STILL found in list after delete!")
        return False
    print("Document successfully removed from list.")
    
    # Clean up local file
    try:
        os.remove(dummy_filename)
    except:
        pass
        
    return True

if __name__ == "__main__":
    if test_delete_flow():
        print("\nSUCCESS: Delete flow verified.")
        sys.exit(0)
    else:
        print("\nFAILURE: Delete flow failed.")
        sys.exit(1)
