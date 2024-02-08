import sqlite3
from flask import Flask, g

from formula.formula import run_formula

app = Flask(__name__)

DATABASE = "database.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def hello_world():
    return "Hello, world!"


@app.route("/cells")
def list_cells():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM cells;")
    return [{"id": cell[0], "formula": cell[1]} for cell in cur.fetchall()]


@app.route("/cells/<id>")
def get_cell(id=None):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM cells WHERE id=?", (id,))
    cell = cur.fetchone()
    print(cell)
    return {"id": cell[0], "formula": run_formula(cell[1])}
