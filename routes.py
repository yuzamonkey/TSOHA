from app import app
from flask import render_template, request, redirect, make_response
import events
import attributes

@app.route("/")
def index():
    counties = attributes.get_counties()
    return render_template("index.html", counties=counties)