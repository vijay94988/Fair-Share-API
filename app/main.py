from fastapi import FastAPI

from app.routers import groups, users

app = FastAPI()

app.include_router(users.router)
app.include_router(groups.router)



# @app.get("/")
# def root():
#     return {"Message": "Fair Share API Is Running"}






# ## Group Members
# @app.get("/group_members")
# def get_group_members():
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT * FROM group_members;")
#             group_members = cursor.fetchall()
#             return {"Group Members": group_members}

# @app.get("/group_members/{id}")
# def get_member(id: int):
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT * FROM group_members WHERE group_id = %s", (id,))
#             member = cursor.fetchone()
#             if not member:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group member not found")
#             return member


# @app.post("/group_members", status_code=status.HTTP_201_CREATED)
# def add_group_member(group_member: GroupMemberCreate):
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             try:
#                 cursor.execute(
#                     "INSERT INTO group_members(group_id, user_id) VALUES (%s, %s) RETURNING *",
#                     (group_member.group_id, group_member.user_id)
#                 )
#                 members = cursor.fetchone()
#                 return members
#             except UniqueViolation:
#                 raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group member already exists")


# @app.delete("/groups/{group_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_member(group_id: int, user_id: int):
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute(
#                 "DELETE FROM group_members WHERE group_id = %s AND user_id = %s RETURNING *",
#                 (group_id, user_id)
#             )
#             deleted_member = cursor.fetchone()
#             if not deleted_member:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found")



# ## Expenses
# @app.get("/expenses")
# def get_expenses():
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT * FROM expenses;")
#             expenses = cursor.fetchall()
#             return {"Expenses": expenses}

# @app.get("/expenses/{id}")
# def get_expense(id: int):
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT * FROM expenses WHERE id = %s", (id,))
#             expense = cursor.fetchone()
#             if not expense:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
#             return expense


# @app.post("/expenses", status_code=status.HTTP_201_CREATED)
# def create_expense(expense:ExpenseCreate):
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             # Checking if group exists
#             cursor.execute("SELECT 1 FROM groups WHERE id = %s",
#             (expense.group_id,))
#             if not cursor.fetchone():
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

#             #Checking if user exists
#             cursor.execute("SELECT 1 FROM users WHERE id = %s",
#             (expense.created_by,))
#             if not cursor.fetchone():
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#             cursor.execute(
#                 "INSERT INTO expenses(group_id, description, total_amount, created_by) VALUES (%s, %s, %s, %s) RETURNING *",
#                 (expense.group_id, expense.description, expense.total_amount, expense.created_by)
#             )
#             expense_data = cursor.fetchone()
#             return expense_data

# @app.put("/expenses/{id}")
# def update_expense(id: int, expense:ExpenseCreate):
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute(
#                 "UPDATE expenses SET group_id = %s, description = %s, total_amount = %s, created_by = %s WHERE id = %s RETURNING *",
#                 (expense.group_id, expense.description, expense.total_amount, expense.created_by, id)
#             )
#             updated_expense = cursor.fetchone()
#             if not updated_expense:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense ID not found")
            
#             print({"Message": "Expense Updated"})
#             return updated_expense


# @app.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_expense(id: int):
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute(
#                 "DELETE FROM expenses WHERE id = %s RETURNING id",
#                 (id,)
#             )
#             deleted_expense = cursor.fetchone()
#             if not deleted_expense:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")



# ## Expense Splits
# @app.get("/expense_splits")
# def get_expense_splits():
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT * FROM expense_splits;")
#             expense_splits = cursor.fetchall()
#             return {"Expense Splits": expense_splits}

# @app.get("/expense_splits/{id}")
# def get_split(id: int):
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT * FROM expense_splits WHERE expense_id = %s", (id,))
#             split = cursor.fetchone()
#             if not split:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Split not found")
#             return split


# ## Expense Payers
# @app.get("/expense_payers")
# def get_expense_payers():
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT * FROM expense_payers;")
#             expense_payers = cursor.fetchall()
#             return {"Expense Payers": expense_payers}

# @app.get("/expense_payers/{id}")
# def get_payer(id: int):
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT * FROM expense_payers WHERE expense_id = %s", (id,))
#             payer = cursor.fetchone()
#             if not payer:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payer not found")
#             return payer


# ## Settle ups
# @app.get("/settle_ups")
# def get_settle_ups():
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT * FROM settle_ups;")
#             settle_ups = cursor.fetchall()
#             return {"Settle Ups": settle_ups}

# @app.get("/settle_ups/{id}")
# def get_settle_up(id: int):
#     with my_pool.connection() as conn:
#         with conn.cursor(row_factory=dict_row) as cursor:
#             cursor.execute("SELECT * FROM settle_ups WHERE id = %s", (id,))
#             settle_up = cursor.fetchone()
#             if not settle_up:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settle_Up not found")
#             return settle_up
