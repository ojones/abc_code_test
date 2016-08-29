import random
import uuid

from flask import Flask, render_template, request, g

from abc_code import db, score

app = Flask(__name__)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():

    questions = db.query_db('select * from questions')
    test_idxs = random.sample(set(range(0, len(questions))), 3)
    test_set = list()
    for idx in test_idxs:
        test_set.append(questions[idx])

    return render_template('questions.html',
                           questions=test_set)


@app.route('/scores')
def all_scores():

    scores = db.query_db('select * from scores')

    return render_template('scores.html',
                           scores=scores)


@app.route('/complete', methods=['POST'])
def complete():
    # map answers to question id at the end of form key name
    answers = dict((key.replace('answer_', ''),
                    request.form.getlist(key)) for key in request.form.keys())

    # get in memory map of all questions and points for displaying results
    questions = db.query_db('select * from questions')
    questions_map = dict()
    for question in questions:
        questions_map[question['id']] = (question['question'], question['points'])

    # collect score for each question in test scores list
    test_scores = []
    test_id = str(uuid.uuid4())[:5]
    for question_id in answers:
        answer = answers[question_id][0]
        test_scores.append(score.score_answer(question_id, answer, test_id))

    # send test score list to view
    return render_template('complete.html',
                           scores=test_scores)











