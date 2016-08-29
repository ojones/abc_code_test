from __future__ import division

import math
import string
import uuid

import db

from nltk import PorterStemmer
from nltk.corpus import stopwords

cachedStopWords = stopwords.words("english")


def choose_score(question_id, criteria_id):
        score = 0
        row = db.query_db('select * from questions where id = ?',
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
        if ordered_count == len(keywords) or ordered_count > 2:
            criteria = 'criteria-1'
        elif unordered_count > 1:
            criteria = 'criteria-2'
        elif unordered_count > 0:
            criteria = 'criteria-3'
        else:
            criteria = 'criteria-4'
        return criteria


def preprocess_words(words):
    exclude = set(string.punctuation)
    words = [''.join(ch for ch in x if ch not in exclude) for x in words.lower().split()]
    white_list = ['if', 'then', 'for', 'while', 'unitl', 'not', 'on']
    black_list = [x for x in cachedStopWords if x not in white_list]
    stemmed = [PorterStemmer().stem_word(x) for x in words]
    approved = [x for x in stemmed if x not in black_list]
    return approved


def score_answer(question_id, answer, test_id, score_table='scores', print_only=False):
        # get in memory map of all questions and points for displaying results
        questions = db.query_db('select * from questions')
        questions_map = dict()
        for question in questions:
            questions_map[question['id']] = (question['question'], question['points'])

        # get all keyword sets
        rows = db.query_db('select * from keywords where question_id = ?', [question_id])

        answered_words = preprocess_words(answer)

        # evaluate answered words against each set of answer keywords
        points = 0
        criteria_id = ''
        for row in rows:
            keywords = preprocess_words(row['ordered_keywords'])
            tmp_criteria_id = choose_criteria(keywords, answered_words)
            tmp_points = choose_score(question_id, tmp_criteria_id)
            # keep only the highest point value and corresponding criteria id
            if tmp_points > points:
                points = tmp_points
                criteria_id = tmp_criteria_id

        # save score to database
        fields = ('id', 'test_id', 'question_id', 'answered', 'score', 'criteria_id')
        values = (str(uuid.uuid4())[:5], test_id, question_id, answer, points, criteria_id)

        if not print_only:
            db.insert(score_table, fields=fields, values=values)
        else:
            print(points)

        # create score dict with added fields for display purposes and append to test scores list
        score_dict = dict()
        for idx, key in enumerate(fields):
            score_dict[key] = values[idx]
            if key == 'question_id':
                score_dict['question'], score_dict['points_possible'] = questions_map[question_id]

        return score_dict
