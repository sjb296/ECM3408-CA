import sys
from flask import Flask

from formula.formula import eval_formula, valid_formula

app = Flask(__name__)

if len(sys.argv) < 3 or (sys.argv[1] == "-r" and sys.argv[2] == "sqlite"):
    from db.sqlite_helper import *
elif sys.argv[1] == "-r" and sys.argv[2] == "firebase":
    from db.firebase_helper import *

app.add_url_rule("/cells", view_func=list_cells, methods=["GET"])
app.add_url_rule("/cells/<id>", view_func=get_cell, methods=["GET"])
app.add_url_rule("/cells/<id>", view_func=create_cell, methods=["PUT"])
app.add_url_rule("/cells/<id>", view_func=delete_cell, methods=["DELETE"])


if __name__ == "__main__":
    app.run(port=3000)
