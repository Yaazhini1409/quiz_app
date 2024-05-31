from flask import Flask, render_template, request, session, redirect, url_for, flash, send_file

from services.qa_services import get_no_of_question_list, get_question_count, get_qns, update_question, \
    update_no_of_question
from services.quiz_services import get_quiz_id, get_data, get_quizzes, add_quiz, get_quiz_name
from services.user_auth import update_user, check_user
from services.score_manager import get_score_date, calculate_score, update_score, get_finish, get_user_score, \
    update_list, display_score
from services.user_services import get_user_id, get_user_list

import datetime

from services.utils import get_name_org, get_edit, generate_pdf_from_html, get_num

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route('/', methods=['GET', 'POST'])
def wel():
    if request.method == 'POST':
        if request.form['start'] == 'login':
            email = request.form['email']

            print("Email: ", email)
            password = request.form['password']
            check = check_user(email, password)
            if check[0]:
                id = get_user_id(email)
                if id == 1:
                    details = get_name_org(email)
                    print("details", details)
                    session['username'] = details[0][0]
                    session['org'] = details[0][1]
                    session['scorelist'] = []
                    session['score'] = 0
                    session['answers'] = []
                    qn = 1
                    session['user'] = check[1]
                    print("main", session['user'])
                    return redirect(url_for('choose'))
                else:
                    session['passage'] = 1
                    return redirect(url_for('admin'))
            else:
                flash('Wrong email or password. Make sure you are registered.', 'error')
                return render_template('login.html')
        else:
            return redirect(url_for('reg'))
    else:
        session['passage'] = 0
        return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        name = request.form['Name']
        session['username'] = name
        org = request.form['org']
        session['org'] = org
        email = request.form['email']
        password = request.form['Password']
        check = update_user(name, org, email, password)
        if not check:
            flash('You are already registered. Login to continue', 'error')
            return render_template('reg.html')
        else:
            session['user'] = check
            session['email'] = email
            session['scorelist'] = []
            session['score'] = 0
            session['answers'] = []
            qn = 1
            return redirect(url_for('choose'))
    else:
        return render_template('reg.html')


@app.route('/choose', methods=['GET', 'POST'])
def choose():
    if request.method == 'POST':
        session['scorelist'] = []
        session['score'] = 0
        session['answers'] = []
        quiz = request.form['quiz']
        session['id'] = get_quiz_id(quiz)
        session['name'] = quiz
        qn = 1
        return redirect(url_for('quiz', qn=qn, id=session['id']))

    else:
        count = get_no_of_question_list()
        print("count", count)
        scorelist = get_score_date(session['user'])
        print("scorelist", scorelist)
        return render_template('choose.html', table=scorelist, count=count)


@app.route('/quiz/<int:qn>/<int:id>', methods=['GET', 'POST'])
def quiz(qn, id):
    global answer
    count = get_question_count(id)
    answers = {}
    print("initial:", qn)
    if request.method == 'POST':

        for key, value in request.form.items():
            if value:
                if key.startswith('Answer_'):
                    question_id = key.split('_')[1]
                    answers[question_id] = value.split('_')[0]
                    print("qno", value.split('_'))
                    session['scorelist'] = calculate_score(answers, qn)
                    print("scorelist", session['scorelist'])
                    print("selected option: ", key.split('_'))
                    option = value.split('_')[1]
                    session['answers'] = update_list(qn, option)
                    print("session ", session['answers'])
            else:
                session['scorelist'] = calculate_score(answers, qn)
                print(session['scorelist'])

        if qn <= count:

            # print("after increment:", qn)
            row = get_data(qn, id)
            # print("question:", row)
            if request.form['but_ton'] == 'prev':
                # print("current qn", qn)
                return redirect(url_for('quiz', qn=qn - 1, id=id))
            elif request.form['but_ton'] == 'next':
                # print("cn qn", qn)
                return redirect(url_for('quiz', qn=qn + 1, id=id))
            else:
                return redirect(url_for('result'))

        else:

            return redirect(url_for('result'))
    else:

        row = get_data(qn, id)
        print("Question ", row)
        answer = session.get('answers')
        if answer:
            print("session", answer)
            if len(answer) >= qn:
                print("qn: ", qn - 1)
                ans = answer[qn - 1]
                print("Ans: ", ans)
                if ans != 0:
                    an = ans['Answer']
                else:
                    an = ""
            else:
                an = ""

        else:
            an = ""
        return render_template('quiz.html', question=row, qn=qn, count=count, answer=an)


@app.route('/result')
def result():
    count = get_num(session['id'])
    score = 0
    scores = session.get('scorelist', [])
    print("score", scores)
    print("count", count[0][0])
    for i in range(0, count[0][0]):
        if scores[i] is not None:
            score += scores[i]
        else:
            score += 0

    print("Score: ", score)
    print("user: ", session['user'])
    print("QuizID: ", session['id'])
    print("name: ", session['name'])
    update_score(score, session['user'], session['id'], session['name'])

    return render_template('result.html', score=score)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session['passage'] == 1:
        return render_template('admin.html')
    else:
        return render_template('login.html')


@app.route('/admin/score')
def score():
    table = display_score()
    return render_template('score.html', table=table)


@app.route('/admin/user')
def user():
    table = get_user_list()
    return render_template('user.html', table=table)


@app.route('/admin/qui', methods=['GET', 'POST'])
def qui():
    if request.method == 'POST':
        if request.form['quiz'] == "add":
            return redirect(url_for('add'))
        elif request.form['quiz'] == "addqn":
            return redirect(url_for('AddQuestion'))
        else:
            for key, value in request.form.items():
                session['quiz'] = value
                print("value ", value)
                qn_id = get_quiz_id(value)
                print("qn_id", qn_id)
                session['id'] = qn_id
                return redirect('/admin/qui/qns')
    else:
        table = get_quizzes()
        return render_template('quizchoice.html', table=table)


@app.route('/admin/qui/qns')
def qnss():
    if request.method == 'POST':
        if request.form['quiz'] == "addqn":
            return redirect(url_for('AddQuestion'))
    else:
        table = get_qns(session['id'])
        return render_template('questions.html', table=table)


@app.route('/edit/<qn>', methods=["GET", "POST"])
def edit(qn):
    if request.method == "POST":
        num = request.form['number']
        question = request.form['qn']
        one = request.form['one']
        two = request.form['two']
        three = request.form['three']
        four = request.form['four']
        ans = request.form['ans']
        update_question(num, question, one, two, three, four, ans, session['quiz'], session['id'])
        flash('Question updated successfully')
        return redirect('/admin/qui/qns')
    else:
        table = get_edit(session['id'], qn)[0]
        return render_template('edit.html', table=table, qn=qn)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":

        name = request.form['name']

        add_quiz(name)
        flash('Quiz added successfully')
        return redirect('/admin/qui')
    else:
        return render_template('add.html')


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == "POST":
        print("session", session['id'])
        num = request.form['number']
        question = request.form['qn']
        one = request.form['one']
        two = request.form['two']
        three = request.form['three']
        four = request.form['four']
        ans = request.form['ans']
        add_question(num, question, one, two, three, four, ans, session['quiz'], session['id'])
        update_no_of_question(num, session['quiz'])
        flash('Question added successfully')
        return redirect('/admin/qui/qns')
    else:
        return render_template('AddQuestion.html')


@app.route('/certificate/<quiz_id>')
def certificate(quiz_id):
    session['quizname'] = get_quiz_name(quiz_id)
    session['score'] = get_user_score(session['quizname'], session['user'])
    session['number'] = get_num(quiz_id)
    if not session['score']:
        flash('Attend the quiz to get certificate', 'error')
        count = get_question_count()
        scorelist = get_score_date(session['user'])
        return render_template('choose.html', table=scorelist, count=count)
    else:
        date = datetime.date.today()
        finish = get_finish(session['user'], quiz_id)

        print("finish", finish)

        def generate_pdf_from_html(html_content, output_file_path):
            # Open the output file in binary write mode
            with open(output_file_path, "wb") as pdf_file:
                # Write the PDF header

                pdf_file.write(html_content.encode())

            # Print a message to indicate successful PDF generation
            print("PDF generated successfully.")

        output_file_path = session['username'] + str(date) + ".html"
        html_content = render_template("content.html", name=session['username'], org=session['org'],
                                       q=session["quizname"],
                                       score=session['score'], date=finish, num=session['number'])
        generate_pdf_from_html(html_content, output_file_path)
        return send_file(output_file_path, as_attachment=True)
