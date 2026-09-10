import os
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

if not db_name or not db_user or not db_password:
    raise RuntimeError("Database environment variables are missing")
