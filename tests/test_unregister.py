"""Tests for DELETE /activities/{activity_name}/unregister endpoint"""
import pytest


def test_unregister_existing_participant(client):
    """Test successful unregister of an existing participant"""
    # Get an existing participant
    response = client.get("/activities")
    email_to_remove = response.json()["Chess Club"]["participants"][0]
    
    # Unregister
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email_to_remove}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email_to_remove in data["message"]


def test_unregister_participant_is_removed(client):
    """Test that participant is actually removed from activity"""
    # Get initial state
    response = client.get("/activities")
    initial_participants = response.json()["Chess Club"]["participants"].copy()
    initial_count = len(initial_participants)
    email_to_remove = initial_participants[0]
    
    # Unregister
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email_to_remove}
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    updated_participants = response.json()["Chess Club"]["participants"]
    
    assert len(updated_participants) == initial_count - 1
    assert email_to_remove not in updated_participants


def test_unregister_nonexistent_participant_fails(client):
    """Test that unregistering non-existent participant returns 400"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"]


def test_unregister_invalid_activity_fails(client):
    """Test that unregistering from non-existent activity returns 404"""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "test@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_then_unregister_cycle(client):
    """Test complete signup and unregister cycle"""
    email = "cycletest@mergington.edu"
    
    # Sign up
    response = client.post(
        "/activities/Gym Class/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify added
    response = client.get("/activities")
    assert email in response.json()["Gym Class"]["participants"]
    
    # Unregister
    response = client.delete(
        "/activities/Gym Class/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify removed
    response = client.get("/activities")
    assert email not in response.json()["Gym Class"]["participants"]


def test_signup_again_after_unregister(client):
    """Test that a student can sign up again after unregistering"""
    email = "resignup@mergington.edu"
    
    # Sign up
    response = client.post(
        "/activities/Basketball Team/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Unregister
    response = client.delete(
        "/activities/Basketball Team/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Sign up again (should succeed)
    response = client.post(
        "/activities/Basketball Team/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify in participants
    response = client.get("/activities")
    assert email in response.json()["Basketball Team"]["participants"]
