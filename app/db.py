import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Use Row objects to return results of queries
        g.db.row_factory = sqlite3.Row

    return g.db

def query_db(query, args=(), one=False):
    """ Execute a SQL query and return the result. """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_sql(query, args=()):
    """ Execute a SQL command against the database. """
    cur = get_db().cursor()
    cur.execute(query, args)
    get_db().commit()
    cur.close()

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)
