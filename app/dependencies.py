from app.database import my_pool

def get_db_cursor():
    with my_pool.connection() as conn, conn.cursor() as cursor:
        yield cursor
