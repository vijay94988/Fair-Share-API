from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation

from app.database import my_pool
from app.models.schemas import ExpenseSplitCreate

router = APIRouter()

@router.get("/expense_splits")
def get_expense_splits():
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM expense_splits;")
            expense_splits = cursor.fetchall()
            return {"Expense Splits": expense_splits}

@router.get("/expense_splits/{id}", )
def get_split(id: int):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM expense_splits WHERE expense_id = %s", (id,))
            split = cursor.fetchone()
            if not split:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Split not found")
            return split


@router.post("/expense_splits", status_code=status.HTTP_201_CREATED)
def create_split(split:ExpenseSplitCreate):
    with my_pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            ""
        )

