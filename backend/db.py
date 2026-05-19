import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="try1",
        user="postgres",
        password="1234567",
        port=5432
    )