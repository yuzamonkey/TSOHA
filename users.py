from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session


def log_in(username, password):
    user = db.session.execute(
        f"SELECT password, id FROM Users WHERE username='{username}'").fetchone()
    if (not user):
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["user_id"] = user[1]
            return True
        else:
            return False


def log_out():
    del session["user_id"]


def add_user(username, password):
    password = generate_password_hash(password)
    try:
        db.session.execute(
            f"INSERT INTO Users (username, password, admin, suspended) VALUES ('{username}','{password}', {False}, {False})")
        db.session.commit()
        return True
    except:
        print("ERROR, USERNAME TAKEN")
        return False
