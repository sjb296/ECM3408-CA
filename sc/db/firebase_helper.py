import requests
import os
from flask import request

from formula.formula import eval_formula, valid_formula

URL = os.environ["FBASE"]
params = '?orderBy="$key"&startAt="B1"&limitToFirst=1'


def list_cells():
    """Return a JSON list containing the coordinates of all cells#
    that have data in them"

    e.g. `["B1, "C6", ...]`
    """
    res = requests.get(URL + ".json")
    if res.ok:
        if res.json() == None:
            return "", 200
        else:
            return res.json()
    else:
        return "", 500


def get_cell(id):
    """Given the label of a cell, return a JSON object containing
    the data stored in the cell

    e.g. `{"formula", "6"}`"""
    params = f'?orderBy="$key"&startAt="{id}"&limitToFirst=1'
    res = requests.get(URL + ".json" + params)
    formula = list(res.json().values())[0]

    # print(res.json())

    if res.json() == None:
        return "", 404
    elif res.ok:
        # print(f"Formula {formula}")
        if valid_formula(formula):
            formula_result = eval_formula(formula)
        else:
            return "", 500

        return {"formula": f"{formula_result}"}
    else:
        return "", 500


def create_cell(id=None):
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
    exists = requests.get(URL + ".json" + params)
    if exists.ok and exists.json() != None:
        updated = True
    else:
        updated = False

    res = requests.patch(
        URL + ".json", f'{{ "{req_json["id"]}": "{req_json["formula"]}" }}'
    )
    if res.ok:
        if updated:
            return "", 204
        else:
            return "", 201
    else:
        print(res.json())
        return "", 500


def delete_cell(id):
    """Delete a cell with a given label."""
    # Check it exists
    code = list(get_cell(id).values())[0]
    if not code:
        return "", 404

    res = requests.delete(URL + f"{id}.json")

    if res.json() == None:  # deletion returns null
        return "", 200
    else:
        return "", 500
