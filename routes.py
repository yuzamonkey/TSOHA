from app import app
from flask import render_template, request, redirect, session, make_response 
import attributes
import events
import users


@app.route("/")
def index():
    #filters
    if request.args:
        category = request.args["category"]
        county = request.args["county"]
        if (category and not county):
            selected_events = events.get_all_filter_by_category(attributes.get_category_id(category))
        if (county and not category):
            selected_events = events.get_all_filter_by_county(attributes.get_county_id(county))
        if (county and category):
            selected_events = events.get_all_filter_by_category_and_county(attributes.get_category_id(category), attributes.get_county_id(county)) 
        else: 
            selected_events = events.get_all()
    else:
        selected_events = events.get_all()

    categories = attributes.get_categories()
    counties = attributes.get_counties()
    return render_template("index.html", events=selected_events, categories=categories, counties=counties)

# users
@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    if request.method == "GET":
        return render_template("log_in.html", error=False)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if (users.log_in(username, password)):
            return redirect("/")
        else:
            return render_template("log_in.html", error=True, message="Tarkista käyttäjätunnus tai salasana")

@app.route("/user_info")
def user_info():
    user_id = users.session["user_id"]
    username = users.get_username(user_id)
    users_events = events.get_events_by_user_id(user_id)
    return render_template("user_info.html", username=username, users_events=users_events)

@app.route("/edit_username", methods=["GET", "POST"])
def edit_username():
    user_id = users.session["user_id"]
    username = users.get_username(user_id)
    if request.method == "GET":
        return render_template("edit_username.html", username=username, error=False)
    if request.method == "POST":
        new_username = request.form["new_username"]
        print("NEW USERNAME == ", new_username)
        if (users.edit_username(new_username, user_id)):
            return redirect("/user_info")
        else:
            return render_template("edit_username.html", username=username, error=True, message="Käyttäjätunnus on varattu")

@app.route("/edit_password", methods=["GET", "POST"])
def edit_password():
    user_id = users.session["user_id"]
    if request.method == "GET":
        return render_template("edit_password.html")
    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        if (users.verify_current_password(current_password, user_id)):
            if (users.edit_password(new_password, user_id)):
                return redirect("/user_info")
            else:
                return render_template("edit_password.html", error=True, message="Päivittäminen epäonnistui")
        else:
            return render_template("edit_password.html", error=True, message="Syötit nykyisen salasanasi väärin")

@app.route("/log_out")
def log_out():
    users.log_out()
    return redirect("/")

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("sign_up.html", error=False)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if (users.sign_up(username, password)):
            print("SUCCESS")
            return redirect("/")
        else:
            print("FAIL")
            return render_template("sign_up.html", error=True)

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "GET":
        return render_template("report.html")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        attributes.send_report(title, content)
        return render_template("report.html", message="Kiitos viestistäsi")

# events
@app.route("/event/<int:id>")
def event(id):
    event = events.get_event_by_id(id)
    image_id = events.get_image_id(id)
    return render_template("event.html", event=event, image_id=image_id)

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

@app.route("/edit_event/<int:id>", methods=["GET", "POST"])
def edit_event(id):
    if request.method == "GET":
        event = events.get_event_by_id(id)
        event_category = attributes.get_category_name(event[3])
        event_county = attributes.get_county_name(event[4])
        categories = attributes.get_categories()
        counties = attributes.get_counties()
        starting_time = attributes.timestamp_to_datetime(event[-4])
        ending_time = attributes.timestamp_to_datetime(event[-3])
        print(f"STARTING AT {starting_time} ENDING AT {ending_time}")
        return render_template(
            "edit_event.html", 
            event=event, 
            event_category=event_category, 
            event_county=event_county, 
            categories=categories, 
            counties=counties,
            starting_time=starting_time,
            ending_time=ending_time
            )
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

        events.edit_event(
            id,
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
        )
        return redirect("/user_info")

@app.route("/delete_event/<int:id>", methods=["GET", "POST"])
def delete_event(id):
    events.delete_event(id)
    if users.session["is_admin"]:
        return redirect("/admin_page")
    else:
        return redirect("/user_info")


#admin
@app.route("/admin_page")
def admin_page():
    if not users.session["is_admin"]:
        return "No access"
    else:
        usernames = users.get_all_users_id_username_suspend()
        all_events = events.get_all()
        reports = attributes.get_reports()
        user_count = users.user_count()
        event_count = events.event_count()
        return render_template("admin_page.html", usernames=usernames, events=all_events, reports=reports, user_count=user_count, event_count=event_count)

@app.route("/delete_report/<int:id>")
def delete_report(id):
    attributes.delete_report(id)
    return redirect("/admin_page")

@app.route("/suspend_user/<int:id>")
def suspend_user(id):
    users.suspend(id)
    return redirect("/admin_page")

@app.route("/remove_suspension/<int:id>")
def remove_suspension(id):
    users.remove_suspension(id)
    return redirect("/admin_page")

@app.route("/delete_user/<int:id>")
def delete_user(id):
    users.delete(id)
    return redirect("/admin_page")