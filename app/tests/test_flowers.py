def test_add_and_get_flowers(client):
    # Добавляем цветок
    response = client.post("/flowers", json={
        "name": "Rose",
        "quantity": 10,
        "price": 5.0
    })
    assert response.status_code == 200
    flower_id = response.json()["id"]

    # Получаем список цветов
    response = client.get("/flowers")
    assert response.status_code == 200
    assert any(f["id"] == flower_id for f in response.json())

