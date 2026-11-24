"""Smoke test for the local demo API. Run after `python seed.py` and `python app.py`."""
import requests
BASE_URL = "http://127.0.0.1:5000/api"

def run():
    s = requests.Session()
    login = s.post(f"{BASE_URL}/login", json={"email": "demo@learvix.com", "password": "Learvix@123"}, timeout=10)
    assert login.status_code == 200, f"Login failed: {login.status_code} {login.text}"
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    for endpoint in ("/me", "/users", "/matches", "/exchanges", "/notifications"):
        response = s.get(BASE_URL + endpoint, headers=headers, timeout=10)
        assert response.status_code == 200, f"{endpoint}: {response.status_code} {response.text}"
        print(f"PASS {endpoint}")
    me = s.get(BASE_URL + "/me", headers=headers, timeout=10).json()
    assert me["email"] == "demo@learvix.com"
    print("All API smoke checks passed.")

if __name__ == "__main__":
    run()
