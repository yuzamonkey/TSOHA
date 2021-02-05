from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session


def log_in(username, password):
    sql = "SELECT password, id, username, admin, suspended FROM Users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()
    if (not user):
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["user_id"] = user[1]
            session["username"] = user[2]
            session["is_admin"] = user[3]
            session["suspended"] = user[4]
            return True
        else:
            return False

def log_out():
    del session["user_id"]
    del session["is_admin"]

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

def edit_username(new_username, id):
    sql = "UPDATE Users SET username=:new_username WHERE id=:id"
    try:
        db.session.execute(sql, {"new_username":new_username,"id":id})
        db.session.commit()
        return True
    except:
        return False

def verify_current_password(password, id):
    sql = "SELECT password FROM Users WHERE id=:id"
    current_password = db.session.execute(sql, {"id":id}).fetchone()[0]
    if (check_password_hash(current_password, password)):
        return True
    else:
        return False

def edit_password(new_password, id):
    new_password = generate_password_hash(new_password)
    sql = "UPDATE Users SET password=:new_password WHERE id=:id"
    try:
        db.session.execute(sql, {"new_password":new_password, "id":id})
        db.session.commit()
        return True
    except:
        return False

def get_all_users_id_username_suspend():
    sql = "SELECT id, username, suspended FROM Users ORDER BY username"
    result = db.session.execute(sql).fetchall()
    return result

def get_user_count():
    sql = "SELECT COUNT(*) FROM USERS"
    count = db.session.execute(sql).fetchone()[0]
    return count

def remove_suspension(id):
    sql = f"UPDATE USERS SET Suspended={False} WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def suspend(id):
    sql = f"UPDATE USERS SET Suspended={True} WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def delete(id):
    sql = "DELETE FROM Users WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
