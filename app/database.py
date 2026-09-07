import os
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool


load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

if not db_name or not db_user or not db_password:
    raise RuntimeError("Database environment variables are missing")

conn_info = f"host=localhost dbname={db_name} user={db_user} password={db_password}"


my_pool = ConnectionPool(
        conn_info,
        open=True,
        min_size=3,
        max_size=8
)
