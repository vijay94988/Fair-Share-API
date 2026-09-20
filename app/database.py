import psycopg_pool
from fastapi import HTTPException, status
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from app.config import db_name, db_user, db_password

conn_info = f"host=localhost dbname={db_name} user={db_user} password={db_password}"

my_pool = ConnectionPool(
        conn_info,
        open=True,
        min_size=0,
        max_size=8,
        timeout=10,
        kwargs={"row_factory": dict_row}
)

# Dependency
def get_db_cursor():
        try:
                with my_pool.connection() as conn, conn.cursor() as cursor:
                        yield cursor
        except psycopg_pool.PoolTimeout:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="DB down!!!!")

