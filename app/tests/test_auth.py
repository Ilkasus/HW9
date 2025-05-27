def test_signup_and_login(client):
    response = client.post("/signup", data={
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "secret"
    })
    assert response.status_code == 200

    response = client.post("/login", data={
        "username": "test@example.com",
        "password": "secret"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

