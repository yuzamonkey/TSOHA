from app import app
from flask import render_template, request, redirect, make_response

from db import db



@app.route("/")
def index():
    sql = ("SELECT * FROM Counties")
    counties = db.session.execute(sql).fetchall()
    print("COUNTIES === ", counties)
    return render_template("index.html", counties=counties)