import os
from random import shuffle
from flask import Flask, render_template, request, redirect, url_for
from db_scripts import get_question_after, get_quizes, check_answer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FULL'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['quiz'] = request.form.get('quiz')
        session['last_question'] = 0
        session['total'] = 0
        session['correct'] = 0
        return redirect(url_for('test'))
    else:
        return quiz_form()

@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'quiz' not in session or int(session['quiz']) < 0:
        return redirect(url_for('index'))

    if request.method == 'POST':
        save_answer()

    next_question = get_question_after(session['last_question'], session['quiz'])
    if next_question is None or len(next_question) == 0:
        return redirect(url_for('result'))
    else:
        return question_form(next_question)

@app.route('/result')
def result():
    html = render_template('result.html', right=session['correct'], total=session['total'])
    session.clear()
    return html

def quiz_form():
    q_list = get_quizes()
    return render_template('start.html', q_list=q_list)

def save_answer():
    answer = request.form.get('ans_text')
    qu_id = request.form.get('q_id')
    session['last_question'] = qu_id
    session['total'] += 1
    if check_answer(qu_id, answer):
        session['correct'] += 1

def question_form(question):
    answer_list = [question[2], question[3], question[4], question[5]]
    shuffle(answer_list)
    return render_template('test.html', question=question[1], quiz_id=question[0], answers_list=answer_list)

if __name__ == '__main__':
    app.run()
