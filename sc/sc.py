import sys
from flask import Flask

from db_helper import *

if len(sys.argv) < 3 or (sys.argv[1] == "-r" and sys.argv[2] == "sqlite"):
    db = SqliteHelper()
elif sys.argv[1] == "-r" and sys.argv[2] == "firebase":
    db = FirebaseHelper()

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


app.add_url_rule("/cells", view_func=db.list_cells, methods=["GET"])
app.add_url_rule("/cells/<id>", view_func=db.get_cell, methods=["GET"])
app.add_url_rule("/cells/<id>", view_func=db.create_cell, methods=["PUT"])
app.add_url_rule("/cells/<id>", view_func=db.delete_cell, methods=["DELETE"])


if __name__ == "__main__":
    app.run(port=3000)
