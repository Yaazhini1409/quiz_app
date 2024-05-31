import psycopg2
from flask import session

from services.utils import count
from connections import conn
import psycopg2.extras


def check_user(email, password):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    QUERY = """SELECT "ID", "Password" FROM "User" WHERE "Email" = %s"""
    cur.execute(QUERY, (email,))
    c = cur.fetchall()
    if not c:
        return [False]
    session['user_id'] = c[0][0]
    q = """SELECT * FROM "User" where "Password" = crypt(%s, "Password")"""
    cur.execute(q, (password,))
    passwrd = cur.fetchall()
    print("passwrd", passwrd)
    if passwrd:
        return [True, session['user_id']]
    return [False]


def update_user(name, org, email, password):
    id = count() + 1
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    quer = """SELECT * FROM "User" WHERE "Email" = %s """
    cur.execute(quer, (email,))
    c = cur.fetchall()
    if c:
        return False
    else:
        Query = """INSERT INTO "User" ("ID", "Name", "Organisation", "Email","id") VALUES (%s, %s,%s,%s,1)"""
        cur.execute(Query, (id, name, org, email))
        session['user_id'] = id
        conn.commit()
        q = """update "User" set "Password" = crypt(%s, gen_salt('md5')) Where "ID" = %s"""
        cur.execute(q, (password, id))
        conn.commit()
        return session['user_id']
