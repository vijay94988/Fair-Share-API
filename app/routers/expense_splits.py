from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_db_cursor

router = APIRouter()

@router.get("/expense_splits")
def get_expense_splits(cursor=Depends(get_db_cursor)):
    cursor.execute("SELECT * FROM expense_splits;")
    expense_splits = cursor.fetchall()
    return {"Expense Splits": expense_splits}


@router.get("/expense_splits/{id}", )
def get_split(id: int, cursor=Depends(get_db_cursor)):
    cursor.execute("SELECT * FROM expense_splits WHERE expense_id = %s", (id,))
    split = cursor.fetchall()
    if not split:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Split not found")
    return split