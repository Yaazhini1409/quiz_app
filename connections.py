import psycopg2
import psycopg2.extras


def create_connection():
    try:
        conn = psycopg2.connect(
            host="host",
            database="database",
            port=5432,
            user="user",
            password="password"
        )
        return conn
    except psycopg2.Error as e:
        print("Error :", e)
        return None


conn = create_connection()
