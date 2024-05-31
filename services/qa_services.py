import psycopg2

from connections import conn
import psycopg2.extras


def get_correct_answers():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    QUERY = """SELECT "ID", "Answer" FROM "Question" """
    cur.execute(QUERY)
    rows = cur.fetchall()
    return {row['ID']: row['Answer'] for row in rows}


def get_question_count(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    QUERY = """SELECT COUNT(*) FROM "Question" WHERE "QuizID" = %s"""
    cur.execute(QUERY, (id,))
    count = cur.fetchall()[0][0]
    print(count)
    return count


def get_qns(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "Q_no", "Question", "Option_1", "Option_2", "Option_3", "Option_4", "Answer" from "Question" where "QuizID" = %s order by "Q_no" """
    cur.execute(query, (id,))
    table = cur.fetchall()
    return table


def get_no_of_question_list():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "NoOfQns" from "Quiz" order by "ID" """
    cur.execute(query)
    c = cur.fetchall()
    return c


def update_no_of_question(num, name):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """update "Quiz" set "NoOfQns" = %s where "QuizName" = %s"""
    cur.execute(query, (num, name,))
    conn.commit()


def add_question(num, qn, one, two, three, four, ans, name, id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """insert into "Question" ("Question", "Option_1", "Option_2","Option_3","Option_4", "Answer", "QuizID", "Q_no", "Quizname") values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(query, (qn, one, two, three, four, ans, id, num, name))
    conn.commit()


def update_question(num, qn, one, two, three, four, ans, name, id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """update "Question" set "Question" = %s, "Option_1" = %s, "Option_2" = %s,"Option_3" = %s,"Option_4" = %s, "Answer" = %s where "Q_no" = %s and "QuizID" = %s """
    cur.execute(query, (qn, one, two, three, four, ans, num, id,))
    conn.commit()
