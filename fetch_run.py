import requests
import json

BASE_URL = "https://disease-detection-backend-asag.onrender.com/api/v1"

def login():
    res = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "hqml@gmail.com", "password": "12345678"}
    )
    if res.status_code == 200:
        return res.json()["access_token"]
    
    print(f"Login failed: {res.text}")
    return None

def get_run(token, run_id):
    res = requests.get(
        f"{BASE_URL}/training/{run_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    if res.status_code == 200:
        return res.json()
    print(f"Fetch failed: {res.text}")
    return None

token = login()
if token:
    run_id = "6abf768b602f1085a9bbd3b3"
    print(f"Logged in. Fetching run {run_id}...")
    run_data = get_run(token, run_id)
    if run_data:
        print(json.dumps(run_data, indent=2))
