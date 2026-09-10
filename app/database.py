from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from app.config import db_name, db_user, db_password

conn_info = f"host=localhost dbname={db_name} user={db_user} password={db_password}"

my_pool = ConnectionPool(
        conn_info,
        open=True,
        min_size=3,
        max_size=8,
        kwargs={"row_factory": dict_row}
)
