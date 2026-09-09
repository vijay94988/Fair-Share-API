from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row

from app.database import my_pool
from app.models.schemas import SettleUpCreate

router = APIRouter()

@router.get("/settle_ups")
def get_settle_ups():
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM settle_ups;")
            settle_ups = cursor.fetchall()
            return {"Settle Ups": settle_ups}

@router.get("/settle_ups/{id}")
def get_settle_up(id: int):
    with my_pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT * FROM settle_ups WHERE id = %s", (id,))
            settle_up = cursor.fetchone()
            if not settle_up:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settle_Up not found")
            return settle_up
