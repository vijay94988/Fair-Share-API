from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row

from app.database import my_pool
from app.models.schemas import ExpenseCreate

router = APIRouter()

@router.get("/expenses")
def get_expenses():
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM expenses;")
            expenses = cursor.fetchall()
            return {"Expenses": expenses}

@router.get("/expenses/{id}")
def get_expense(id: int):
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM expenses WHERE id = %s", (id,))
            expense = cursor.fetchone()
            if not expense:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
            return expense


@router.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(expense:ExpenseCreate):
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            # Checking if group exists
            cursor.execute("SELECT 1 FROM groups WHERE id = %s",
            (expense.group_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

            #Checking if user exists
            cursor.execute("SELECT 1 FROM users WHERE id = %s",
            (expense.created_by,))
            if not cursor.fetchone():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            cursor.execute(
                "INSERT INTO expenses(group_id, description, total_amount, created_by) VALUES (%s, %s, %s, %s) RETURNING *",
                (expense.group_id, expense.description, expense.total_amount, expense.created_by)
            )
            expense_data = cursor.fetchone()
            return expense_data

@router.put("/expenses/{id}")
def update_expense(id: int, expense:ExpenseCreate):
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "UPDATE expenses SET group_id = %s, description = %s, total_amount = %s, created_by = %s WHERE id = %s RETURNING *",
                (expense.group_id, expense.description, expense.total_amount, expense.created_by, id)
            )
            updated_expense = cursor.fetchone()
            if not updated_expense:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense ID not found")
            
            print({"Message": "Expense Updated"})
            return updated_expense


@router.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int):
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "DELETE FROM expenses WHERE id = %s RETURNING id",
                (id,)
            )
            deleted_expense = cursor.fetchone()
            if not deleted_expense:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
