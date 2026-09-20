from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_db_cursor

router = APIRouter()


@router.get("/expense_payers")
def get_expense_payers(cursor=Depends(get_db_cursor)):
    cursor.execute("SELECT * FROM expense_payers;")
    expense_payers = cursor.fetchall()
    return {"Expense Payers": expense_payers}


@router.get("/expense_payers/{id}")
def get_payer(id: int, cursor=Depends(get_db_cursor)):
    cursor.execute("SELECT * FROM expense_payers WHERE expense_id = %s", (id,))
    payer = cursor.fetchall()
    if not payer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payer not found")
    return payer