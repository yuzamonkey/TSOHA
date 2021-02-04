from db import db
from werkzeug.security import check_password_hash, generate_password_hash

def add_user(username, password):
    password = generate_password_hash(password)
    try:
        db.session.execute(f"INSERT INTO Users (username, password, admin, suspended) VALUES ('{username}','{password}', {False}, {False})")
        db.session.commit()
        return True
    except:
        print("ERROR, USERNAME TAKEN")
        return False
