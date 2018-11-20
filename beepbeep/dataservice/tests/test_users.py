import unittest
from beepbeep.dataservice.database import User

def test_init_db(db):
    q = db.session.query(User).filter().first()
    assert q.email == 'example@example.com', "A first user with email 'example@example.com' should be defined"

def test_create_user(db, client):
    r = client.post("/users", json={
        "age": 22,
        "email": "test@example.com",
        "firstname": "Testss",
        "lastname": "Test",
        "max_hr": 180,
        "rest_hr": 50,
        "strava_token": "83cd6be4e00abfec6aead223d2ac77ca9ea3247e",
        "vo2max": 63.0,
        "weight": 60.0
    })
    assert r.status_code == 201, "Create user should return 201"

def test_create_user_wrong_body(db, client):
    r = client.post("/users", json={
        "age": "22",
        "email": "test@example.com",
        "firstname": "Testss",
        "lastname": "Test",
        "max_hr": 180,
        "rest_hr": 50,
        "strava_token": "83cd6be4e00abfec6aead223d2ac77ca9ea3247e",
        "vo2max": 63.0,
        "weight": 60.0
    })
    assert r.status_code == 400, "Raise a 400"

def test_create_user_missing_body(db, client):
    r = client.post("/users")
    assert r.status_code == 400, "Raise a 400"

def test_duplicate_email_create_user(db, client):
    r = client.post("/users", json={
        "age": 22,
        "email": "test@example.com",
        "firstname": "Testss",
        "lastname": "Test",
        "max_hr": 180,
        "rest_hr": 50,
        "strava_token": "null",
        "vo2max": 63.0,
        "weight": 60.0
    })
    assert r.status_code == 400, "Cannot create user with duplicated email"

def test_get_users(db, client):
    r = client.get("/users")
    users = r.get_json()
    assert r.status_code == 200, "Should return the users list"
    assert len(users) == 2, "Should return 2 users"

def test_get_user_by_id(db, client):
    r = client.get("/users/2")
    user = r.get_json()
    assert r.status_code == 200, "Should return the user with 200 status code"
    assert user['id'] == 2, "Should return user 2"
    assert user['email'] == "test@example.com", "Should return the user test@example.com"

def test_get_user_404(db, client):
    r = client.get("/users/666")
    assert r.status_code == 404, "Missing user should return 404"

def test_get_user_missing_id(db, client):
    r = client.get("/users/")
    user = r.get_json()
    assert r.status_code == 404, "Should return 404 status code"

def test_update_user(db, client):
    r = client.put("/users/2", json={
		"id": 2,
        "age": 22,
        "email": "up@example.com",
        "firstname": "Testss",
        "lastname": "Test",
        "max_hr": 180,
        "rest_hr": 50,
        "strava_token": "null",
        "vo2max": 63.0,
        "weight": 60.0
    })
    assert r.status_code == 200, "Should update the user"
    user = r.get_json()
    assert user['email'] == "up@example.com", "Should update the user email"

def test_update_user_missing_body(db, client):
    r = client.put("/users/2")
    assert r.status_code == 400, "Raise a 400"

def test_update_404_user(db, client):
    r = client.put("/users/666", json={
		"id": 666,
        "age": 22,
        "email": "up@example.com",
        "firstname": "Testss",
        "lastname": "Test",
        "max_hr": 180,
        "rest_hr": 50,
        "strava_token": "null",
        "vo2max": 63.0,
        "weight": 60.0
    })
    assert r.status_code == 404, "Should return 404"


def test_delete_user_by_id(db, client):
    r = client.delete("/users/2")
    assert r.status_code == 204, "Should return 204"
    r = client.get("/users/2")
    assert r.status_code == 404, "Should have deleted the user"

def test_delete__404_user(db, client):
    r = client.delete("/users/666")
    assert r.status_code == 404, "Should return 404"

def test_delete_user_missing_id(db, client):
    r = client.delete("/users/")
    user = r.get_json()
    assert r.status_code == 404, "Should return 404 status code"