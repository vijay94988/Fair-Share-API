from fastapi import APIRouter, HTTPException, status
from psycopg.errors import UniqueViolation

from app.database import my_pool
from app.models.schemas import GroupCreate

router = APIRouter()

@router.get("/groups")
def get_groups():
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM groups;")
            groups = cursor.fetchall()
            return {"Groups": groups}


@router.get("/groups/{id}")
def get_group(id: int):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM groups WHERE id = %s", (id,))
            group = cursor.fetchone()
            if not group:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
            return group


@router.post("/groups", status_code= status.HTTP_201_CREATED)
def create_group(group: GroupCreate):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO groups (group_name, created_by) VALUES (%s, %s) RETURNING *",
                    (group.group_name, group.created_by)
                )
                group_data = cursor.fetchone()
                return group_data
            except UniqueViolation:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group Already Exists")


@router.put("/groups/{id}")
def update_group(id: int, group: GroupCreate):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute(
                "UPDATE groups SET group_name = %s WHERE id = %s RETURNING *",
                (group.group_name, id)
            )
            updated_group_data = cursor.fetchone()
            if not updated_group_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group ID not found")

            print({"Message": "Group Updated"})
            return updated_group_data


@router.delete("/groups/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(id: int):
    with my_pool.connection() as conn, conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM groups WHERE id = %s RETURNING id",
                (id,)
            )
            deleted_group = cursor.fetchone()
            if not deleted_group:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group ID not found")

