import psycopg2

from connections import conn
import psycopg2.extras


def get_data(qn, id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    QUERY = """SELECT * FROM "Question" WHERE "Q_no" = %s AND "QuizID" = %s"""
    cur.execute(QUERY, (qn, id,))
    rows = cur.fetchone()
    return rows


def get_quiz_id(name):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "ID" from "Quiz" where "QuizName" = %s """
    cur.execute(query, (name,))
    c = cur.fetchall()
    return c


def add_quiz(name):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """insert into "Quiz" ("QuizName") values (%s)"""
    cur.execute(query, (name,))
    conn.commit()


def get_quiz_id(name):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "ID" from "Quiz" where "QuizName" = %s """
    cur.execute(query, (name,))
    c = cur.fetchall()
    print("C", c[0][0])
    return c[0][0]


def get_quizzes():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "ID", "QuizName" from "Quiz" order by "ID" """
    cur.execute(query)
    table = cur.fetchall()
    return table


def get_quiz_count():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    QUERY = """SELECT COUNT(*) FROM "Quiz" """
    cur.execute(QUERY)
    c = cur.fetchone()[0]
    print(c)
    return c


def get_quiz_name(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "QuizName" from "Quiz" where "ID" = %s """
    cur.execute(query, (id,))
    c = cur.fetchall()
    print("name", c[0][0])
    return c[0][0]
