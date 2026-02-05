import requests

url = "http://127.0.0.1:8000/api/upload"
files = {'file': open('test_syllabus.txt', 'rb')}
data = {'department': 'CSE', 'semester': 'S1'}

try:
    response = requests.post(url, files=files, data=data)
    print(response.status_code)
    print(response.json())
except Exception as e:
    print(e)
