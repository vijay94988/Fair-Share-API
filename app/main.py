from fastapi import FastAPI, Response, status, HTTPException
from psycopg.errors import UniqueViolation
from pydantic import BaseModel, EmailStr
from database import my_pool


app = FastAPI()


class UserCreate(BaseModel):
    username: str
    email: EmailStr


class GroupCreate(BaseModel):
    group_name: str
    created_by: int


class GroupMemberCreate(BaseModel):
    group_id: int
    user_id: int


class ExpenseCreate(BaseModel):
    id: int
    group_id: int
    description: str
    total_amount: int
    created_by: int



@app.get("/")
def root():
    return {"Message": "Fair Share API Is Running"}


@app.get("/users")
def get_users():
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
    return {"Users": users}


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING *",
                    (user.username, user.email)
                )
                user_data = cursor.fetchone()
                return user_data
            except UniqueViolation:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or Email already Exists")


@app.put("/users/{id}")
def update_user(id: int, user: UserCreate):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET username = %s, email = %s WHERE id = %s RETURNING *",
                (user.username, user.email, id)
            )
            updated_user = cursor.fetchone()
            if not updated_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")

            print({"Message": "User Updated"})
            return updated_user


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM users WHERE id = %s RETURNING id",
                (id,)
            )
            deleted_user = cursor.fetchone()
            if not deleted_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")



## Groups:
@app.get("/groups")
def get_groups():
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM groups;")
            groups = cursor.fetchall()
            return {"Groups": groups}


@app.post("/groups", status_code= status.HTTP_201_CREATED)
def create_group(group: GroupCreate):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO groups (group_name, created_by) VALUES (%s, %s) RETURNING *",
                    (group.group_name, group.created_by)
                )
                group_data = cursor.fetchone()
                return group_data
            except UniqueViolation:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group Already Exists")


@app.put("/groups/{id}")
def update_group(id: int, group: GroupCreate):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE groups SET group_name = %s WHERE id = %s RETURNING *",
                (group.group_name, id)
            )
            updated_group_data = cursor.fetchone()
            if not updated_group_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group ID not found")

            print({"Message": "Group Updated"})
            return updated_group_data


@app.delete("/groups/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(id: int):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM groups WHERE id = %s RETURNING id",
                (id,)
            )
            deleted_group = cursor.fetchone()
            if not deleted_group:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group ID not found")



## Group Members
@app.get("/group_members")
def get_group_members():
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM group_members;")
            group_members = cursor.fetchall()
            return {"Group Members": group_members}


@app.post("/group_members", status_code=status.HTTP_201_CREATED)
def add_group_member(group_member: GroupMemberCreate):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO group_members(group_id, user_id) VALUES (%s, %s) RETURNING *",
                    (group_member.group_id, group_member.user_id)
                )
                members = cursor.fetchone()
                return members
            except UniqueViolation:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group member already exists")


@app.delete("/group_members/delete_member", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member:GroupMemberCreate):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM group_members WHERE group_id = %s AND user_id = %s RETURNING *",
                (member.group_id, member.user_id)
            )
            deleted_member = cursor.fetchone()
            if not deleted_member:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found")



## Expenses
@app.get("/expenses")
def get_expenses():
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM expenses;")
            expenses = cursor.fetchall()
            return {"Expenses": expenses}


@app.post("/create_expense/{id}", status_code=status.HTTP_201_CREATED)
def create_expense(id:int, expense:ExpenseCreate):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO expenses WHERE id = %s, group_id = %s, description = %s, total_amount = %s, created_by = %s RETURNING *",
                (id, expense.group_id, expense.description, expense.total_amount, expense.created_by)
            )
            expense = cursor.fetchone()
            if not expense:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Details not found")


@app.put("/update_expense/{id}")
def update_expense(id: int, expense:ExpenseCreate):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE expenses SET group_id = %s, description = %s, total_amount = %s, created_by = %s WHERE id = %s, RETURNING *",
                (id, expense.group_id, expense.description, expense.total_amount, expense.created_by)
            )
            updated_expense = cursor.fetchone()
            if not updated_expense:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense ID not found")
            
            print({"Message": "Expense Updated"})
            return updated_expense


@app.delete("/delete_expense/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int):
    with my_pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE expense WHERE id = %s RETURNING *",
                (id,)
            )
            deleted_expense = cursor.fetchone()
            if not deleted_expense:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense ID not found")


