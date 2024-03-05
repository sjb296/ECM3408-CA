rm -rf venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install flask
python3 -m pip install requests
touch sc/database.db
sqlite3 database.db "CREATE TABLE IF NOT EXISTS cells (id, formula);"