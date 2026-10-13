
def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Message": "Fair Share API is Running"}

