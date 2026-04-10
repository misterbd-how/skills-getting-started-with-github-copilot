import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture(scope="module")
def client():
    # Arrange: Create a TestClient for the FastAPI app
    with TestClient(app) as c:
        yield c

def test_get_activities(client):
    # Arrange: (client fixture provides the client)
    # Act: Make a GET request to /activities
    response = client.get("/activities")
    # Assert: Check response status and structure
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()

def test_signup_and_unregister(client):
    # Arrange
    activity = "Art Club"
    email = "testuser@mergington.edu"
    signup_url = f"/activities/{activity}/signup"

    # Act: Sign up for activity (email as query param)
    signup_response = client.post(signup_url, params={"email": email})
    # Assert
    assert signup_response.status_code == 200
    # No participants in response, just message
    assert f"Signed up {email} for {activity}" in signup_response.json()["message"]

    # Act: Unregister from activity (email as query param)
    unregister_response = client.delete(signup_url, params={"email": email})
    # Assert
    assert unregister_response.status_code == 200
    assert f"Removed {email} from {activity}" in unregister_response.json()["message"]

def test_signup_activity_not_found(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser@mergington.edu"
    signup_url = f"/activities/{activity}/signup"
    # Act
    response = client.post(signup_url, params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
