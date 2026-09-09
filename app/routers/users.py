from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row

from app.database import my_pool
from app.models.schemas import UserCreate 


router = APIRouter()


@router.get("/users")
def get_users():
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
    return {"Users": users}

@router.get("/users/{id}")
def get_user(id: int):
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            try:
                cursor.execute(
                    "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING *",
                    (user.username, user.email)
                )
                user_data = cursor.fetchone()
                return user_data
            except UniqueViolation:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or Email already Exists")


@router.put("/users/{id}")
def update_user(id: int, user: UserCreate):
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "UPDATE users SET username = %s, email = %s WHERE id = %s RETURNING *",
                (user.username, user.email, id)
            )
            updated_user = cursor.fetchone()
            if not updated_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")

            print({"Message": "User Updated"})
            return updated_user


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "DELETE FROM users WHERE id = %s RETURNING id",
                (id,)
            )
            deleted_user = cursor.fetchone()
            if not deleted_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")

