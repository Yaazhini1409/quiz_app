import psycopg2
import psycopg2.extras

from flask import session

from connections import conn
from services.qa_services import get_correct_answers


def calculate_score(answers, qn):
    correct_answers = get_correct_answers()
    # print(correct_answers)
    for key, value in answers.items():

        scores = session.get('scorelist', [])
        if len(scores) < qn:
            scores.extend([0] * (qn - len(scores)))
        if value:
            if value == correct_answers[int(key)]:
                scores[qn - 1] = 1
            else:
                scores[qn - 1] = 0
        else:
            scores[qn - 1] = 0
    print(session['scorelist'])
    return session['scorelist']


def update_score(score, userid, id, name):
    print("userid", userid)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """SELECT * FROM "Userscore" WHERE "UserID" = %s AND "QuizID" = %s"""
    cur.execute(query, (userid, id,))
    c = cur.fetchall()
    if c:
        quer = """UPDATE "Userscore" SET "Score" = %s, "CreatedDate" = default WHERE "UserID" = %s AND "QuizID" = %s"""
        cur.execute(quer, (score, userid, id))
        conn.commit()
    else:
        Query = """INSERT INTO "Userscore" ("Score" , "UserID","QuizID","Quizname" ) VALUES (%s, %s, %s, %s) """
        cur.execute(Query, (score, userid, id, name))
        conn.commit()


def get_score_date(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    QUERY = """ SELECT Q."ID" AS "QuizID", Q."NoOfQns", Q."QuizName", US."Score", US."CreatedDate", U."ID" AS UserID FROM public."Quiz" Q LEFT JOIN public."Userscore" US ON Q."ID" = US."QuizID"  AND (US."UserID" = %s OR US."UserID" IS NULL) Left JOIN public."User" U ON US."UserID" = U."ID" """
    cur.execute(QUERY, (id,))
    c = cur.fetchall()
    return c


def get_finish(name, id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "CreatedDate" from "Userscore" where "UserID" = %s and "QuizID" = %s """
    cur.execute(query, (name, id))
    c = cur.fetchone()
    date_only = c[0]
    return date_only.date()


def get_user_score(quizname, userid):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "Score" from "Userscore" where "UserID" = %s and "Quizname" = %s """
    cur.execute(query, (userid, quizname,))
    c = cur.fetchall()
    if c:
        return c[0][0]
    else:
        return False


def update_list(qn, option):
    ans = session.get('answers', {})
    if len(ans) < qn:
        ans.extend([0] * (qn - len(ans)))
    print("option in func", option)
    ans[qn - 1] = {"Answer": option}
    return session['answers']


def display_score():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    Query = """ SELECT U."Name", U."Organisation", U."Email" , US."Quizname", US."Score" FROM public."User" AS U JOIN public."Userscore" AS US ON U."ID" = US."UserID" """
    cur.execute(Query)
    table = cur.fetchall()
    return table
