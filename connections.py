import psycopg2
import psycopg2.extras


def create_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            port=5432,
            user="postgres",
            password="Nero7Cami13"
        )
        return conn
    except psycopg2.Error as e:
        print("Error :", e)
        return None


conn = create_connection()
