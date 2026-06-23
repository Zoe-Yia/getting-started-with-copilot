"""Tests for POST /activities/{activity_name}/signup endpoint"""
import pytest


def test_signup_new_participant(client):
    """Test successful signup of a new participant"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_participant_is_added(client):
    """Test that participant is actually added to activity"""
    # Get initial state
    response = client.get("/activities")
    initial_participants = response.json()["Chess Club"]["participants"].copy()
    initial_count = len(initial_participants)
    
    # Sign up new participant
    new_email = "testuser@mergington.edu"
    client.post(
        "/activities/Chess Club/signup",
        params={"email": new_email}
    )
    
    # Verify participant was added
    response = client.get("/activities")
    updated_participants = response.json()["Chess Club"]["participants"]
    
    assert len(updated_participants) == initial_count + 1
    assert new_email in updated_participants


def test_signup_duplicate_email_fails(client):
    """Test that signing up with duplicate email returns 400 error"""
    # Get an existing participant
    response = client.get("/activities")
    existing_email = response.json()["Chess Club"]["participants"][0]
    
    # Try to sign up with same email
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": existing_email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_invalid_activity_fails(client):
    """Test that signing up for non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "test@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_multiple_different_participants(client):
    """Test that multiple different participants can sign up"""
    emails = [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu",
    ]
    
    for email in emails:
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify all were added
    response = client.get("/activities")
    participants = response.json()["Programming Class"]["participants"]
    
    for email in emails:
        assert email in participants
