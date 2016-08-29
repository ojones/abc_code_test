import sqlite3
from flask import g

DATABASE = 'abc_code.db'


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


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def init_db(app):
    with app.app_context():
        database = get_db()
        with app.open_resource('create_schema.sql', mode='r') as f:
            database.cursor().executescript(f.read())
        database.commit()