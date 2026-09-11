from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation

from app.database import my_pool
from app.models.schemas import GroupMemberCreate

router = APIRouter()

@router.get("/group_members")
def get_group_members():
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM group_members;")
            group_members = cursor.fetchall()
            return {"Group Members": group_members}

@router.get("/group_members/{id}")
def get_member(id: int):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM group_members WHERE group_id = %s", (id,))
            member = cursor.fetchone()
            if not member:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group member not found")
            return member


@router.post("/group_members", status_code=status.HTTP_201_CREATED)
def add_group_member(group_member: GroupMemberCreate):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO group_members(group_id, user_id) VALUES (%s, %s) RETURNING *",
                    (group_member.group_id, group_member.user_id)
                )
                members = cursor.fetchone()
                return members
            except UniqueViolation:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group member already exists")


@router.delete("/groups/{group_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(group_id: int, user_id: int):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM group_members WHERE group_id = %s AND user_id = %s RETURNING *",
                (group_id, user_id)
            )
            deleted_member = cursor.fetchone()
            if not deleted_member:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found")
