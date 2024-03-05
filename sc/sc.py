import sys
from flask import Flask

# from db.db import list_cells, get_cell, create_cell, delete_cell
from db_helper import *

if len(sys.argv) < 3 or (sys.argv[1] == "-r" and sys.argv[2] == "sqlite"):
    db = SqliteHelper()
elif sys.argv[1] == "-r" and sys.argv[2] == "firebase":
    db = FirebaseHelper()

app = Flask(__name__)


app.add_url_rule("/cells", view_func=db.list_cells, methods=["GET"])
app.add_url_rule("/cells/<id>", view_func=db.get_cell, methods=["GET"])
app.add_url_rule("/cells/<id>", view_func=db.create_cell, methods=["PUT"])
app.add_url_rule("/cells/<id>", view_func=db.delete_cell, methods=["DELETE"])


if __name__ == "__main__":
    app.run(port=3000)
