import sqlite3
import sys
from flask import Flask, g, request

from formula.formula import run_formula, valid_formula

DATABASE = "database.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# @app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# @app.route("/")
def hello_world():
    return "Hello, world!"


# @app.route("/cells")
def list_cells():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM cells;")
    return [cell[0] for cell in cur.fetchall()]


# @app.route("/cells/<id>", methods=["GET"])
def get_cell(id=None):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM cells WHERE id=?", (id,))
    cell = cur.fetchone()
    if cell:
        return {"id": cell[0], "formula": run_formula(cell[1])}
    else:
        return "", 404


# @app.route("/cells/<id>", methods=["PUT"])
def create_cell(id=None):
    json = request.get_json()

    if json["id"] != id:
        return "", 400
    elif not json["formula"] or not valid_formula(json["formula"]):
        return "", 400

    # Create the record
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO cells (id, formula) VALUES (?, ?);", (json["id"], json["formula"])
    )
    db.commit()

    # Check if the new record exists
    cur.execute(
        "SELECT * FROM cells WHERE id=? AND formula=?;", (json["id"], json["formula"])
    )
    if cur.fetchone():
        return "", 201
    else:
        return "", 500


# @app.route("/cells/<id>", methods=["DELETE"])
def delete_cell(id=None):
    db = get_db()
    cur = db.cursor()

    # Check the cell exists
    cur.execute("SELECT * FROM cells WHERE id=?;", (id,))
    if not cur.fetchone():
        return "", 404

    # Delete the record
    cur.execute("DELETE FROM cells WHERE id=?", (id,))
    db.commit()

    return "", 204
