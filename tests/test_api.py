import time
import requests
from tests.conftest import BASE_URL, get_auth_token


def test_health_endpoint_returns_healthy():
    """Test that the health endpoint returns status 200 and healthy status."""
    response = requests.get(f"{BASE_URL}/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user_creates_new_user():
    """Test that registering a new user returns 201 and the correct username."""
    username = f"testuser_{int(time.time())}"
    data = {
        "username": username,
        "password": "testpassword"
    }

    response = requests.post(f"{BASE_URL}/api/auth/register", json=data)

    assert response.status_code == 201
    assert response.json()["user"]["username"] == username


def test_login_returns_jwt_token():
    """Test that logging in with valid credentials returns 200 and a JWT access token."""
    username = f"loginuser_{int(time.time())}"
    password = "testpassword"

    requests.post(f"{BASE_URL}/api/auth/register", json={"username": username, "password": password})

    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": username, "password": password})

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_public_event_requires_auth_and_succeeds_with_token():
    """Test that creating an event with a valid token returns 201 and correct event data."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    event_data = {
        "title": "Test Event",
        "description": "A test event",
        "date": "2026-06-15T18:00:00",
        "location": "Test Location",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    response = requests.post(f"{BASE_URL}/api/events", json=event_data, headers=headers)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Test Event"
    assert body["date"] == "2026-06-15T18:00:00"
    assert body["is_public"] is True


def test_rsvp_to_public_event_succeeds_without_auth():
    """Test that an unauthenticated user can RSVP to a public event."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    event_data = {
        "title": "Public RSVP Test Event",
        "date": "2026-07-01T18:00:00",
        "is_public": True,
    }

    event_response = requests.post(f"{BASE_URL}/api/events", json=event_data, headers=headers)
    event_id = event_response.json()["id"]

    response = requests.post(f"{BASE_URL}/api/rsvps/event/{event_id}", json={"attending": True})

    assert response.status_code == 201
    assert response.json()["event_id"] == event_id
    assert response.json()["attending"] is True


def test_duplicate_username_registration_returns_400():
    """Test that registering with an already taken username returns 400."""
    username = f"duplicate_{int(time.time())}"
    data = {"username": username, "password": "testpassword"}

    response1 = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    assert response1.status_code == 201

    response2 = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["error"]


def test_create_event_without_auth_returns_401():
    """Test that creating an event without authentication returns 401."""
    event_data = {
        "title": "Unauthorized Event",
        "date": "2026-08-01T18:00:00",
    }

    response = requests.post(f"{BASE_URL}/api/events", json=event_data)

    assert response.status_code == 401


def test_rsvp_to_non_public_event_without_auth_returns_401():
    """Test that RSVPing to a non-public event without authentication returns 401."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    event_data = {
        "title": "Private Event",
        "date": "2026-08-01T18:00:00",
        "is_public": False,
    }

    event_response = requests.post(f"{BASE_URL}/api/events", json=event_data, headers=headers)
    event_id = event_response.json()["id"]

    response = requests.post(f"{BASE_URL}/api/rsvps/event/{event_id}", json={"attending": True})

    assert response.status_code == 401
    assert "Authentication required" in response.json()["error"]