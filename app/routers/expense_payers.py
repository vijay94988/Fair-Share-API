from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation

from app.database import my_pool
from app.models.schemas import ExpensePayerCreate

router = APIRouter()

@router.get("/expense_payers")
def get_expense_payers():
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM expense_payers;")
            expense_payers = cursor.fetchall()
            return {"Expense Payers": expense_payers}

@router.get("/expense_payers/{id}")
def get_payer(id: int):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM expense_payers WHERE expense_id = %s", (id,))
            payer = cursor.fetchone()
            if not payer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payer not found")
            return payer