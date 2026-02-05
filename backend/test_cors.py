
import requests

def test_cors():
    url = "http://127.0.0.1:8000/api/chat"
    headers = {
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type"
    }
    
    print(f"Testing OPTIONS {url}")
    try:
        response = requests.options(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Headers:")
        for k, v in response.headers.items():
            print(f"  {k}: {v}")
            
        if "Access-Control-Allow-Origin" in response.headers:
            print("CORS Headers present.")
        else:
            print("WARNING: CORS Headers MISSING in OPTIONS response.")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_cors()
