from __future__ import division
import math
import random
import sqlite3
import uuid
from nltk import PorterStemmer
from flask import Flask, render_template, request, g
app = Flask(__name__)

DATABASE = 'abc_code.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():

    questions = query_db('select * from questions')
    test_idxs = random.sample(set(range(0, len(questions))), 3)
    test_set = list()
    for idx in test_idxs:
        test_set.append(questions[idx])

    return render_template('questions.html',
                           questions=test_set)


@app.route('/scores')
def all_scores():

    scores = query_db('select * from scores')

    return render_template('scores.html',
                           scores=scores)


@app.route('/complete', methods=['POST'])
def complete():
    # map answers to question id at the end of form key name
    answers = dict((key.replace('answer_', ''),
                    request.form.getlist(key)) for key in request.form.keys())

    # get in memory map of all questions and points for displaying results
    questions = query_db('select * from questions')
    questions_map = dict()
    for question in questions:
        questions_map[question['id']] = (question['question'], question['points'])

    # collect score for each question in test scores list
    test_scores = []
    test_id = str(uuid.uuid4())[:5]
    for question_id in answers:
        # get all keyword sets
        rows = query_db('select * from keywords where question_id = ?', [question_id])
        answer = answers[question_id][0]
        answered_words = [PorterStemmer().stem_word(x) for x in answer.split()]

        # evaluate answered words against each set of answer keywords
        points = 0
        criteria_id = ''
        for row in rows:
            keywords = [PorterStemmer().stem_word(x) for x in row['ordered_keywords'].split()]
            tmp_criteria_id = choose_criteria(keywords, answered_words)
            tmp_points = choose_score(question_id, tmp_criteria_id)
            # keep only the highest point value and corresponding criteria id
            if tmp_points > points:
                points = tmp_points
                criteria_id = tmp_criteria_id

        # save score to database
        fields = ('id', 'test_id', 'question_id', 'answered', 'score', 'criteria_id')
        values = (str(uuid.uuid4())[:5], test_id, question_id, answer, points, criteria_id)
        insert('scores', fields=fields, values=values)

        # create score dict with added fields for display purposes and append to test scores list
        score = dict()
        for idx, key in enumerate(fields):
            score[key] = values[idx]
            if key == 'question_id':
                score['question'], score['points_possible'] = questions_map[question_id]
        test_scores.append(score)

    # send test score list to view
    return render_template('complete.html', scores=test_scores)


def choose_score(question_id, criteria_id):
        score = 0
        row = query_db('select * from questions where id = ?',
                       [question_id],
                       one=True)
        possible = row['points']
        level_max = 3
        level = 0
        if criteria_id == 'criteria-1':
            level = 3
        elif criteria_id == 'criteria-2':
            level = 2
        elif criteria_id == 'criteria-3':
            level = 1
        elif criteria_id == 'criteria-4':
            level = 0
        scale = level/level_max
        score = scale * possible
        return int(math.ceil(score))


def choose_criteria(keywords, answered_words):
        criteria = ''
        keyword_idx = 0
        ordered_count = 0
        unordered_count = 0
        for word in answered_words:
            if keyword_idx < len(keywords) and keywords[keyword_idx] == word:
                ordered_count += 1
                keyword_idx += 1
            if word in keywords:
                unordered_count += 1
        if ordered_count == len(keywords):
            criteria = 'criteria-1'
        elif unordered_count > 1:
            criteria = 'criteria-2'
        elif len(answered_words):
            criteria = 'criteria-3'
        else:
            criteria = 'criteria-4'
        return criteria


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert(table, fields=(), values=()):
    # g.db is the database connection
    conn = get_db()
    cur = conn.cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    conn.commit()
    cur.close()
    query = "SELECT last_insert_rowid() " + "from " + table
    last_id = query_db(query, one=True)
    return last_id


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('create_schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))