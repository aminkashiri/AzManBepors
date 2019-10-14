from flask_mysqldb import MySQL
from flask import g , current_app

mysql = MySQL()

def get_db():
    if 'db' not in g:
        g.db = mysql.connection
        # g.db.row_factory =MySQL.row
    return g.db

def close_db():
    db = g.pop('db' , None)

    if db is not None:
        db.close()

import click
from flask.cli import with_appcontext
@click.command('sayhello')
@with_appcontext
def sayhello():
    click.echo('hey you')

def init_app(app):
    mysql.init_app(app)
    # app.teardown_appcontext(close_db)
    app.cli.add_command(sayhello)