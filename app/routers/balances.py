from fastapi import APIRouter, HTTPException, status

from app.database import my_pool

router = APIRouter()


@router.get("/groups/{group_id}/balances")
def get_group_balances(group_id: int):
    with my_pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM groups WHERE id = %s", (group_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Group not found")

        cursor.execute(
            """
            WITH paid_by_user AS (
                SELECT expense_payers.user_id, SUM(expense_payers.amount_paid) AS total_paid
                FROM expenses
                JOIN expense_payers ON expense_payers.expense_id = expenses.id
                WHERE expenses.group_id = %s
                GROUP BY expense_payers.user_id
            ),
            owed_by_user AS (
                SELECT expense_splits.user_id, SUM(expense_splits.amount_owed) AS total_owed
                FROM expenses
                JOIN expense_splits ON expense_splits.expense_id = expenses.id
                WHERE expenses.group_id = %s
                GROUP BY expense_splits.user_id
            )
            SELECT
                group_members.user_id,
                COALESCE(paid_by_user.total_paid, 0) AS total_paid,
                COALESCE(owed_by_user.total_owed, 0) AS total_owed
            FROM group_members
            LEFT JOIN paid_by_user ON paid_by_user.user_id = group_members.user_id
            LEFT JOIN owed_by_user ON owed_by_user.user_id = group_members.user_id
            WHERE group_members.group_id = %s
            ORDER BY group_members.user_id
            """,
            (group_id, group_id, group_id),
        )
        balances = cursor.fetchall()

    for balance in balances:
        balance["balance"] = balance["total_paid"] - balance["total_owed"]

    return {"group_id": group_id, "balances": balances}
