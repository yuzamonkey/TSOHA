from app import app
from flask import render_template, request, redirect, make_response
import attributes
import events
import users


@app.route("/")
def index():
    all_events = events.get_all()
    return render_template("index.html", events=all_events)

# users
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
        return render_template("sign_up.html", error=False)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if (users.add_user(username, password)):
            print("SUCCESS")
            return redirect("/")
        else:
            print("FAIL")
            return render_template("sign_up.html", error=True)

# events
@app.route("/event/<int:id>")
def event(id):
    event = events.get_event_by_id(id)
    image_id = events.get_image_id(id)
    return render_template("event.html", event=event, image_id=image_id)

    #image page

@app.route("/event_image/<int:id>")
def event_image(id):
    image = attributes.get_image_data(id)
    response = make_response(bytes(image))
    response.headers.set("Content-Type","image/jpeg")
    return response

@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    if request.method == "GET":
        categories = attributes.get_categories()
        counties = attributes.get_counties()
        return render_template("create_event.html", categories=categories, counties=counties)

    # insert to db
    if request.method == "POST":
        event_name = request.form["event_name"]
        print("EVENT NAME ", event_name)
        category_id = attributes.get_category_id(request.form["category"])
        print("CATEGORY_ID ", category_id)
        description = request.form["description"]
        print("DESCRIPTION ", description)
        price = request.form["price"]
        print("PRICE ", price)
        county_id = attributes.get_county_id(request.form["county"])
        print("COUNTY_ID ", county_id)
        city = request.form["city"]
        print("CITY ", city)
        locale = request.form["locale"]
        print("LOCALE ", locale)
        address = request.form["address"]
        print("ADDRESS ", address)
        starting_time = request.form["starting_time"]
        print("STARTING TIME ", starting_time)
        ending_time = request.form["ending_time"]
        print("ENDING TIME ", ending_time)
        # handle image
        image = request.files["image"]
        image_name = image.filename
        data = image.read()

        image_id = attributes.add_image_and_return_id(image_name, data)
        #image_id = attributes.get_image_id()

        events.add_event(
            event_name,
            category_id,
            description,
            price,
            county_id,
            city,
            locale,
            address,
            starting_time,
            ending_time,
            image_id
        )

        return redirect("/")
