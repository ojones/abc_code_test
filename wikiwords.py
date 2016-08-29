import random
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask

from abc_code import score

app = Flask(__name__)


def main():
    with app.app_context():
        make_fake_answers('text/conditional_word_pool.txt', 'question-1', 'fake-wiki-words-random')
        # make_fake_answers('text/forloop_word_pool.txt', 'question-5', 'fake-wiki-words-random')


def make_fake_answers(text_file_path, question_id, test_id):
    with open(text_file_path, 'r') as myfile:
        text = myfile.read().replace('\n', '')

    fake_answers = list()
    for idx in range(0, 100):
        words = set(text.split())
        select = random.sample(range(0, 10), 1)[0]
        random_answer = ' '.join(random.sample(words, select))
        fake_answers.append(random_answer)
        print_only = False
        score.score_answer(question_id, random_answer, test_id, score_table='fake_scores', print_only=print_only)


if __name__ == '__main__':
        main()
