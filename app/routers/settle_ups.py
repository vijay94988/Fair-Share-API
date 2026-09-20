from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_db_cursor
from app.models.schemas import SettleUpCreate

router = APIRouter()


@router.get("/settle_ups")
def get_settle_ups(cursor=Depends(get_db_cursor)):
    cursor.execute("SELECT * FROM settle_ups;")
    settle_ups = cursor.fetchall()
    return {"Settle Ups": settle_ups}


@router.get("/settle_ups/{id}")
def get_settle_up(id: int, cursor=Depends(get_db_cursor)):
    cursor.execute("SELECT * FROM settle_ups WHERE id = %s", (id,))
    settle_up = cursor.fetchone()
    if not settle_up:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settle_Up not found")
    return settle_up


@router.post("/settle_ups", status_code=status.HTTP_201_CREATED)
def create_settle_up(settle_up:SettleUpCreate, cursor=Depends(get_db_cursor)):
    cursor.execute(
        "INSERT INTO settle_ups (group_id, from_user_id, to_user_id, amount) VALUES (%s, %s, %s, %s) RETURNING *",
        (
            settle_up.group_id,
            settle_up.from_user_id,
            settle_up.to_user_id,
            settle_up.amount)
        )
    settle_up = cursor.fetchone()
    if not settle_up:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return settle_up