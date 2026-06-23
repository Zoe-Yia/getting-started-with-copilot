"""Tests for GET /activities endpoint"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that /activities returns all available activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Should have activities
    assert len(activities) > 0
    
    # Check for expected activities
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
    ]
    for activity_name in expected_activities:
        assert activity_name in activities


def test_get_activities_structure(client):
    """Test that activities have correct structure"""
    response = client.get("/activities")
    activities = response.json()
    
    # Check structure of first activity
    activity = activities["Chess Club"]
    
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    # Check types
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_participants_are_strings(client):
    """Test that participants list contains email strings"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        participants = activity_data["participants"]
        for participant in participants:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email check
