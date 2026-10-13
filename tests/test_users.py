from unittest.mock import Mock
from psycopg.errors import UniqueViolation


def test_get_users_returns_database_rows(client, mock_cursor: Mock):
    mock_cursor.fetchall.return_value = [
        {"id": 1, "username": "Asha", "email": "asha@example.com"},
        {"id": 2, "username": "Ravi", "email": "ravi@example.com"},
    ]

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == {
        "Users": [
            {"id": 1, "username": "Asha", "email": "asha@example.com"},
            {"id": 2, "username": "Ravi", "email": "ravi@example.com"},
        ]
    }
    mock_cursor.execute.assert_called_once_with("SELECT * FROM users;")


def test_get_user_returns_one_user(client, mock_cursor: Mock):
    mock_cursor.fetchone.return_value = {
        "id": 7,
        "username": "Asha",
        "email": "asha@example.com",
    }

    response = client.get("/users/7")
    assert response.status_code == 200
    assert response.json()["id"] == 7
    assert response.json()["username"] == "Asha"
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM users WHERE id = %s", (7,)
    )


def test_get_user_returns_404_when_missing(client, mock_cursor: Mock):
    mock_cursor.fetchone.return_value = None

    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_create_user_returns_new_user(client, mock_cursor: Mock):
    mock_cursor.fetchone.return_value = {
        "id": 8,
        "username": "Meera",
        "email": "meera@example.com",
    }

    response = client.post(
        "/users",
        json={"username": "Meera", "email": "meera@example.com"},
    )
    assert response.status_code == 201
    assert response.json()["id"] == 8
    sql, parameters = mock_cursor.execute.call_args.args
    assert "INSERT INTO users" in sql
    assert parameters == ("Meera", "meera@example.com")


def test_create_user_returns_409_for_duplicate_user(client, mock_cursor: Mock):
    mock_cursor.execute.side_effect = UniqueViolation("duplicate user")

    response = client.post(
        "/users",
        json={"username": "Meera", "email": "meera@example.com"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Username or Email already Exists"}


def test_create_user_rejects_invalid_email_before_database_query(
    client, mock_cursor: Mock
):
    response = client.post(
        "/users",
        json={"username": "Meera", "email": "not-an-email"},
    )
    assert response.status_code == 422
    mock_cursor.execute.assert_not_called()


def test_update_user_returns_updated_user(client, mock_cursor: Mock):
    mock_cursor.fetchone.return_value = {
        "id": 8,
        "username": "Meera Updated",
        "email": "meera.updated@example.com",
    }

    response = client.put(
        "/users/8",
        json={
            "username": "Meera Updated",
            "email": "meera.updated@example.com",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "Meera Updated"
    sql, parameters = mock_cursor.execute.call_args.args
    assert "UPDATE users" in sql
    assert parameters == ("Meera Updated", "meera.updated@example.com", 8)


def test_update_user_returns_404_when_missing(client, mock_cursor: Mock):
    mock_cursor.fetchone.return_value = None

    response = client.put(
        "/users/999",
        json={"username": "Missing", "email": "missing@example.com"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User ID not found"}


def test_delete_user_returns_204(client, mock_cursor: Mock):
    mock_cursor.fetchone.return_value = {"id": 8}

    response = client.delete("/users/8")
    assert response.status_code == 204
    assert response.content == b""
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM users WHERE id = %s RETURNING id", (8,)
    )


def test_delete_user_returns_404_when_missing(client, mock_cursor: Mock):
    mock_cursor.fetchone.return_value = None

    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User ID not found"}
