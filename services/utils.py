import psycopg2
import psycopg2.extras

from connections import conn


def get_name_org(email):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "Name", "Organisation" from "User" where "Email" = %s """
    cur.execute(query, (email,))
    c = cur.fetchall()
    print("name and org", c)
    return c


def get_edit(quiz, no):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select "Question", "Option_1", "Option_2", "Option_3", "Option_4", "Answer" from "Question" where "QuizID" = %s and "Q_no" = %s """
    cur.execute(query, (quiz, no,))
    c = cur.fetchall()
    print("editget", c)
    return c


def count():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    QUERY = """SELECT COUNT(*) FROM "User" """
    cur.execute(QUERY)
    c = cur.fetchone()[0]
    print(c)
    return c


def generate_pdf_from_html(html_content, output_file_path):
    with open(output_file_path, "wb") as pdf_file:
        pdf_file.write(html_content.encode())
    print("PDF generated successfully.")


def get_num(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = """select count(*) from "Question" where "QuizID" = %s """
    cur.execute(query, (id,))
    c = cur.fetchall()
    print("num", c)
    return c
