import sys

if len(sys.argv) < 3 or (sys.argv[1] == "-r" and sys.argv[2] == "sqlite"):
    import db.sqlite_helper

    list_cells = db.sqlite_helper.list_cells
    get_cell = db.sqlite_helper.get_cell
    create_cell = db.sqlite_helper.create_cell
    delete_cell = db.sqlite_helper.delete_cell
elif sys.argv[1] == "-r" and sys.argv[2] == "firebase":
    import db.firebase_helper

    list_cells = db.firebase_helper.list_cells
    get_cell = db.firebase_helper.get_cell
    create_cell = db.firebase_helper.create_cell
    delete_cell = db.firebase_helper.delete_cell
