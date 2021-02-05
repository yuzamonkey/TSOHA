from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session


def log_in(username, password):
    sql = "SELECT password, id FROM Users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()
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

def sign_up(username, password):
    password = generate_password_hash(password)
    try:
        sql = f"INSERT INTO Users (username, password, admin, suspended) VALUES (:username,:password, {False}, {False})"
        db.session.execute(sql, {"username":username, "password":password})
        db.session.commit()
        return True
    except:
        print("ERROR, USERNAME TAKEN")
        return False

def get_username(id):
    sql = "SELECT username FROM Users WHERE id=:id"
    username = db.session.execute(sql, {"id":id}).fetchone()[0]
    return username