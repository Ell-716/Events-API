import time
import requests

BASE_URL = "http://localhost:5000"


def get_auth_token():
    """Register a new user and return a valid JWT token."""
    username = f"user_{int(time.time())}"
    password = "testpassword"

    requests.post(f"{BASE_URL}/api/auth/register", json={"username": username, "password": password})
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": username, "password": password})

    return response.json()["access_token"]
