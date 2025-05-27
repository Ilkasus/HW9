def test_purchase_flow(client):
    # Добавить цветок в корзину
    response = client.post("/cart/items", data={"flower_id": 1})
    assert response.status_code == 200

    # Совершить покупку
    response = client.post("/purchased")
    assert response.status_code == 200

    # Проверить купленные
    response = client.get("/purchased")
    assert response.status_code == 200
    purchases = response.json()
    assert len(purchases) > 0

