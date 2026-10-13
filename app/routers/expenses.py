from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_db_cursor
from app.models.schemas import ExpenseCreate

router = APIRouter()


def validate_expense(expense: ExpenseCreate, cursor):
    participants = expense.participants

    if len(set(participants)) != len(participants):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Participants must be unique")

    if not participants:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Participants are empty")

    cursor.execute("SELECT 1 FROM groups WHERE id = %s", (expense.group_id,))
    if not cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not found")

    cursor.execute("SELECT 1 FROM users WHERE id = %s", (expense.created_by,))
    if not cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found")

    cursor.execute("SELECT user_id FROM group_members WHERE group_id = %s", (expense.group_id,))
    group_member_ids = {row["user_id"] for row in cursor.fetchall()}

    for participant_id in expense.participants:
        if participant_id not in group_member_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Participant not in group")

    for payer in expense.payers:
        if payer.user_id not in group_member_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payer not in group")


@router.get("/expenses")
def get_expenses(cursor=Depends(get_db_cursor)):
    cursor.execute("SELECT * FROM expenses;")
    expenses = cursor.fetchall()
    return {"Expenses": expenses}


@router.get("/expenses/{id}")
def get_expense(id: int, cursor=Depends(get_db_cursor)):
    cursor.execute("SELECT * FROM expenses WHERE id = %s", (id,))
    expense = cursor.fetchone()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


@router.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, cursor=Depends(get_db_cursor)):
    validate_expense(expense, cursor)

    cursor.execute(
        "INSERT INTO expenses(group_id, description, total_amount, created_by) VALUES (%s, %s, %s, %s) RETURNING id",
        (
            expense.group_id,
            expense.description,
            expense.total_amount,
            expense.created_by)
    )
    expense_id = cursor.fetchone()["id"]

    for payer in expense.payers:
        cursor.execute("INSERT INTO expense_payers (expense_id, user_id, amount_paid) VALUES (%s, %s, %s) RETURNING *",
                       (expense_id, payer.user_id, payer.amount_paid))

    share = expense.total_amount / len(expense.participants)

    for participant_id in expense.participants:
        cursor.execute("INSERT INTO expense_splits(expense_id, user_id, amount_owed) VALUES (%s, %s, %s) RETURNING *",
                       (expense_id, participant_id, share))

    return {
        "Expense_ID": expense_id,
        "Message": "Expense created successfully"
    }


@router.put("/expenses/{id}")
def update_expense(id: int, expense: ExpenseCreate, cursor=Depends(get_db_cursor)):
    validate_expense(expense, cursor)

    cursor.execute(
        "UPDATE expenses SET group_id = %s, description = %s, total_amount = %s, created_by = %s WHERE id = %s RETURNING *",
        (expense.group_id, expense.description, expense.total_amount, expense.created_by, id)
    )
    updated_expense = cursor.fetchone()
    if not updated_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense ID not found")

    cursor.execute("DELETE FROM expense_payers WHERE expense_id = %s", (id,))
    for payer in expense.payers:
        cursor.execute("INSERT INTO expense_payers (expense_id, user_id, amount_paid) VALUES (%s, %s, %s) RETURNING *",
                       (id, payer.user_id, payer.amount_paid))

    cursor.execute("DELETE FROM expense_splits WHERE expense_id = %s", (id,))
    share = expense.total_amount / len(expense.participants)

    for participant_id in expense.participants:
        cursor.execute("INSERT INTO expense_splits(expense_id, user_id, amount_owed) VALUES (%s, %s, %s) RETURNING *",
                       (id, participant_id, share))

    print({"Message": "Expense Updated"})
    return updated_expense


@router.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int, cursor=Depends(get_db_cursor)):
    cursor.execute(
        "DELETE FROM expenses WHERE id = %s RETURNING id",
        (id,)
    )
    deleted_expense = cursor.fetchone()
    if not deleted_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
