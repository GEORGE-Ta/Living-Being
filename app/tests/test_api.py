import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_get_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "thinking" in data
    assert "thought_count" in data
    assert "desire_count" in data

def test_add_remove_desire():
    # Add a desire
    desire_data = {
        "description": "Test desire",
        "priority": 1.0,
        "evaluation_criteria": [{
            "type": "keyword",
            "keywords": ["test"],
            "weight": 0.5
        }]
    }
    
    response = client.post("/desires", json=desire_data)
    assert response.status_code == 200
    desire = response.json()
    assert desire["description"] == desire_data["description"]
    
    # Remove the desire
    response = client.delete(f"/desires/{desire['id']}")
    assert response.status_code == 200

def test_get_thoughts():
    response = client.get("/thoughts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_start_stop_thinking():
    # Start thinking
    response = client.post("/start")
    assert response.status_code == 200
    
    # Stop thinking
    response = client.post("/stop")
    assert response.status_code == 200