from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation

from app.database import my_pool
from app.models.schemas import ExpenseCreate

router = APIRouter()

@router.get("/expenses")
def get_expenses():
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM expenses;")
            expenses = cursor.fetchall()
            return {"Expenses": expenses}

@router.get("/expenses/{id}")
def get_expense(id: int):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM expenses WHERE id = %s", (id,))
            expense = cursor.fetchone()
            if not expense:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
            return expense


@router.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            # Validation Checks
            cursor.execute("SELECT 1 FROM groups WHERE id = %s", (expense.group_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

            cursor.execute("SELECT 1 FROM users WHERE id = %s", (expense.created_by,))
            if not cursor.fetchone():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


            cursor.execute(
                "INSERT INTO expenses(group_id, description, total_amount, created_by) VALUES (%s, %s, %s, %s) RETURNING *",
                (
                    expense.group_id,
                    expense.description,
                    expense.total_amount,
                    expense.created_by)
            )
            expense_data = cursor.fetchone()

            expense_id = expense_data["id"]

            # Inserting Payers
            for payer in expense.payers:
                cursor.execute("INSERT INTO expense_payers (expense_id, user_id, amount_paid) VALUES (%s, %s, %s) RETURNING *",
                               (expense_id, payer.user_id, payer.amount_paid)
                               )

            # Calculation and Inserting Splits
            participant_count = len(expense.participants)
            share = expense.total_amount / participant_count


            for participant in expense.participants:
                cursor.execute("INSERT INTO expense_splits(expense_id, user_id, amount_owed) VALUES (%s, %s, %s) RETURNING *",
                               (expense_id, participant, share)
                               )

            return {"Expense_ID": expense_id, "Message": "Expense Created Successfully"}

@router.put("/expenses/{id}")
def update_expense(id: int, expense:ExpenseCreate):
    with my_pool.connection() as conn, conn.cursor() as cursor:
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
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM expenses WHERE id = %s RETURNING id",
                (id,)
            )
            deleted_expense = cursor.fetchone()
            if not deleted_expense:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
