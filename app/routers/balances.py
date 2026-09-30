from fastapi import APIRouter, HTTPException, status

from app.database import my_pool

router = APIRouter()


@router.get("/groups/{group_id}/balances")
def get_group_balances(group_id: int):
    with my_pool.connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM groups WHERE id = %s", (group_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

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
            ),
            sent_by_user AS (
                SELECT from_user_id AS user_id, SUM(amount) AS total_sent
                FROM settle_ups
                WHERE group_id = %s
                GROUP BY from_user_id
            ),
            received_by_user AS (
                SELECT to_user_id AS user_id, SUM(amount) AS total_received
                FROM settle_ups
                WHERE group_id = %s
                GROUP BY to_user_id
            )
            SELECT
                group_members.user_id,
                COALESCE(paid_by_user.total_paid, 0) AS total_paid,
                COALESCE(owed_by_user.total_owed, 0) AS total_owed,
                COALESCE(sent_by_user.total_sent, 0) AS total_sent,
                COALESCE(received_by_user.total_received, 0) AS total_received,
                (
                    COALESCE(paid_by_user.total_paid, 0)
                    - COALESCE(owed_by_user.total_owed, 0)
                    + COALESCE(sent_by_user.total_sent, 0)
                    - COALESCE(received_by_user.total_received, 0)
                ) AS balance
            FROM group_members
            LEFT JOIN paid_by_user ON paid_by_user.user_id = group_members.user_id
            LEFT JOIN owed_by_user ON owed_by_user.user_id = group_members.user_id
            LEFT JOIN sent_by_user ON sent_by_user.user_id = group_members.user_id
            LEFT JOIN received_by_user ON received_by_user.user_id = group_members.user_id
            WHERE group_members.group_id = %s
            ORDER BY group_members.user_id
            """,
            (group_id, group_id, group_id, group_id, group_id),
        )
        balances = cursor.fetchall()

    return {"group_id": group_id, "balances": balances}

