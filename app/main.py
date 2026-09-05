from fastapi import FastAPI, Response, status
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
import time


app = FastAPI()


class UserCreate(BaseModel):
    user_name: str
    email: EmailStr


class GroupCreate(BaseModel):
    group_name: str
    created_by: int

load_dotenv()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
if not db_name or not db_user or not db_password:
    raise RuntimeError("Database environment variables are missing")


while True:
    try:
        conn = psycopg.connect(
            host="localhost",
            dbname=db_name,
            user=db_user,
            password=db_password,
            row_factory=dict_row
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break

    except Exception as error:
        print("Connecting to Database failed")
        print("Error:", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"Message": "Fair Share API Is Running"}


@app.get("/users")
def get_users():
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()

    return {"Users": users}


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING *",
            (user.user_name, user.email)
        )
        user_data = cursor.fetchone()
        conn.commit()
        return user_data
    except Exception as Error:
        conn.rollback()
        print(Error)


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):
    try:
        cursor.execute(
            "UPDATE users SET username = %s, email = %s WHERE id = %s RETURNING *",
            (user.user_name, user.email, user_id)
        )
        updated_user = cursor.fetchone()
        conn.commit()
        print({"Message": "User Updated"})
        return updated_user
    except Exception as Error:
        conn.rollback()
        print(Error)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    try:
        cursor.execute(
            "DELETE FROM users WHERE id = %s",
            (user_id,)
        )
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as Error:
        conn.rollback()
        print(Error)


## Groups:
@app.get("/groups")
def get_groups():
    cursor.execute(
        "SELECT * FROM groups;"
    )
    groups = cursor.fetchall()

    return {"Groups": groups}


@app.post("/groups", status_code= status.HTTP_201_CREATED)
def create_group(group: GroupCreate):
    try:
        cursor.execute(
            "INSERT INTO groups (group_name, created_by) VALUES (%s, %s) RETURNING *",
            (group.group_name, group.created_by)
        )
        group_data = cursor.fetchone()
        conn.commit()
        return group_data
    except Exception as Error:
        conn.rollback()
        print(Error)


@app.put("/groups/{group_id}")
def update_group(group_id: int, group: GroupCreate):
    try:
        cursor.execute(
            "UPDATE groups SET group_name = %s WHERE id = %s RETURNING *",
            (group.group_name, group_id)
        )
        updated_group_data = cursor.fetchone()
        conn.commit()
        return updated_group_data
    except Exception as Error:
        conn.rollback()
        print(Error)


@app.delete("/groups/{group_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int):
    try:
        cursor.execute(
            "DELETE FROM groups WHERE id = %s RETURNING *",
            (group_id,)
        )
        conn.commit()
        return Response(status_code= status.HTTP_204_NO_CONTENT)
    except Exception as Error:
        conn.rollback()
        print(Error)

