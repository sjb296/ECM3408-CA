import sys
from flask import Flask

from db.db import list_cells, get_cell, create_cell, delete_cell
from formula.formula import eval_formula, valid_formula

app = Flask(__name__)


app.add_url_rule("/cells", view_func=list_cells, methods=["GET"])
app.add_url_rule("/cells/<id>", view_func=get_cell, methods=["GET"])
app.add_url_rule("/cells/<id>", view_func=create_cell, methods=["PUT"])
app.add_url_rule("/cells/<id>", view_func=delete_cell, methods=["DELETE"])


if __name__ == "__main__":
    app.run(port=3000)
