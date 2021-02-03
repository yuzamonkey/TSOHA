from app import app
from flask import render_template, request, redirect, make_response
import events
import attributes

@app.route("/")
def index():
    return render_template("index.html")

#users
@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    if request.method == "GET":
        return render_template("log_in.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return redirect("/")

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("sign_up.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return redirect("/")

