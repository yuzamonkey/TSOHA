from db import db
from werkzeug.security import check_password_hash, generate_password_hash

def log_in(username, password):
    user = db.session.execute(f"SELECT password FROM Users WHERE username='{username}'").fetchone()
    if (not user):
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            return True
        else:
            return False




def add_user(username, password):
    password = generate_password_hash(password)
    try:
        db.session.execute(f"INSERT INTO Users (username, password, admin, suspended) VALUES ('{username}','{password}', {False}, {False})")
        db.session.commit()
        return True
    except:
        print("ERROR, USERNAME TAKEN")
        return False
