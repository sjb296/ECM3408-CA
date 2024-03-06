import sqlite3
import os
import requests
from flask import g, request

from formula import eval_formula, valid_formula


class SqliteHelper:
    DATABASE = "database.db"

    def get_db(self):
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(self.DATABASE)
        return db

    def close_connection(self, exception):
        db = getattr(g, "_database", None)
        if db is not None:
            db.close()

    def hello_world(self):
        return "Hello, world!"

    def list_cells(self):
        """Return a JSON list containing the coordinates of all cells#
        that have data in them"

        e.g. `["B1, "C6", ...]`
        """
        cur = self.get_db().cursor()
        cur.execute("SELECT * FROM cells;")
        cells = [cell[0] for cell in cur.fetchall()]
        if cells:
            return f"{cells}"
        else:
            return "[]", 200

    def get_cell(self, id=None):
        """Given the label of a cell, return a JSON object containing
        the label and the data stored in the cell

        e.g. `{"B1", "6"}`"""
        cur = self.get_db().cursor()
        cur.execute("SELECT * FROM cells WHERE id=?", (id,))
        cell = cur.fetchone()
        if cell:
            return {"formula": f"{eval_formula(self, cell[1])}"}
        else:
            return "", 404

    def create_cell(self, id=None):
        """Create a cell with the given label and data. If it
        already exists, update it"""
        db = self.get_db()
        cur = db.cursor()
        json = request.get_json()

        # Check both fields are present and valid
        if "id" not in json or "formula" not in json:
            return "", 400

        if json["id"] != id:
            return "", 400
        elif not json["formula"] or not valid_formula(json["formula"]):
            return "", 400

        # Check if the record exists
        cur.execute("SELECT * FROM cells WHERE id=?;", (json["id"],))
        if cur.fetchone():
            # Update the record
            print("Updating record...")
            cur.execute(
                "UPDATE cells SET formula=? WHERE id=?;", (json["formula"], json["id"])
            )
            db.commit()
            ok_status = 204

        else:
            # Create the record
            print("Creating record...")
            cur.execute(
                "INSERT INTO cells (id, formula) VALUES (?, ?);",
                (json["id"], json["formula"]),
            )
            db.commit()
            ok_status = 201

        # Check if the new record exists
        cur.execute(
            "SELECT * FROM cells WHERE id=? AND formula=?;",
            (json["id"], json["formula"]),
        )
        if cur.fetchone():
            return "", ok_status
        else:
            return "", 500

    def delete_cell(self, id=None):
        """Delete a cell with a given label."""
        db = self.get_db()
        cur = db.cursor()

        # Check the cell exists
        cur.execute("SELECT * FROM cells WHERE id=?;", (id,))
        if not cur.fetchone():
            return "", 404

        # Delete the record
        cur.execute("DELETE FROM cells WHERE id=?", (id,))
        db.commit()

        return "", 204


class FirebaseHelper:
    URL = (
        f"https://{os.environ['FBASE']}-default-rtdb.europe-west1.firebasedatabase.app/"
    )
    params = '?orderBy="$key"&startAt="B1"&limitToFirst=1'

    def list_cells(self):
        """Return a JSON list containing the coordinates of all cells
        that have data in them"

        e.g. `["B1, "C6", ...]`
        """
        res = requests.get(self.URL + ".json")
        if res.ok:
            if res.json() == None:
                return "[]", 200
            else:
                result = list(res.json().keys())
                return f"{result}"
        else:
            return "", 500

    def get_cell(self, id):
        """Given the label of a cell, return a JSON object containing
        the data stored in the cell

        e.g. `{"formula", "6"}`"""
        params = f'?orderBy="$key"&startAt="{id}"&limitToFirst=1'
        res = requests.get(self.URL + ".json" + params)
        formula = list(res.json().values())[0]

        # print(res.json())

        if res.json() == None:
            return "", 404
        elif res.ok:
            # print(f"Formula {formula}")
            if valid_formula(formula):
                formula_result = eval_formula(self, formula)
            else:
                return "", 500

            return {"formula": f"{formula_result}"}
        else:
            return "", 500

    def create_cell(self, id=None):
        """Create a cell with the given label and data. If it
        already exists, update it"""
        req_json = request.get_json()

        # Check both fields are present and valid
        if "id" not in req_json or "formula" not in req_json:
            return "", 400

        if req_json["id"] != id:
            return "", 400
        elif not req_json["formula"] or not valid_formula(req_json["formula"]):
            return "", 400

        # Check if the record exists
        params = f'?orderBy="$key"&startAt="{id}"&limitToFirst=1'
        exists = requests.get(self.URL + ".json" + params)
        if exists.ok and exists.json() != None:
            updated = True
        else:
            updated = False

        res = requests.patch(
            self.URL + ".json", f'{{ "{req_json["id"]}": "{req_json["formula"]}" }}'
        )
        if res.ok:
            if updated:
                return "", 204
            else:
                return "", 201
        else:
            print(res.json())
            return "", 500

    def delete_cell(self, id):
        """Delete a cell with a given label."""
        # Check it exists
        code = list(self.get_cell(id).values())[0]
        if not code:
            return "", 404

        res = requests.delete(self.URL + f"{id}.json")

        if res.json() == None:  # deletion returns null
            return "", 200
        else:
            return "", 500
