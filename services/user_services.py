import psycopg2
from connections import conn
import psycopg2.extras


def get_user_list():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "ID", "Name", "Organisation", "Email","CreatedDate" from "User" order by "ID" """
    cur.execute(query)
    table = cur.fetchall()
    return table


def get_user_id(email):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    QUERY = """SELECT "id" from "User" Where "Email" = %s"""
    cur.execute(QUERY, (email,))
    id = cur.fetchall()
    return id[0][0]
