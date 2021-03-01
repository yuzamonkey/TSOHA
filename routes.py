from app import app
from flask import render_template, request, redirect, session, make_response, abort
import utils
import events
import users


@app.route("/")
def index():
    # filters
    if request.args:
        category = request.args["category"]
        county = request.args["county"]
        date = request.args["date"]
        print("DATE ", date)
        selected_events = utils.events_to_dictionaries(
            events.get_all_upcoming())
        if (category):
            selected_events = utils.filter_by_category(
                selected_events, category)
        if (county):
            selected_events = utils.filter_by_county(selected_events, county)
        if (date):
            selected_events = utils.filter_by_date(selected_events, date)
    else:
        selected_events = utils.events_to_dictionaries(
            events.get_all_upcoming())
    categories = utils.get_categories()
    counties = utils.get_counties()
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
    users_events = utils.events_to_dictionaries(
        events.get_events_by_user_id(user_id))
    return render_template("user_info.html", user_id=user_id, username=username, users_events=users_events)


@app.route("/edit_username", methods=["GET", "POST"])
def edit_username():
    user_id = users.session["user_id"]
    username = users.get_username(user_id)
    if request.method == "GET":
        return render_template("edit_username.html", username=username, error=False)
    if request.method == "POST":
        if (session["csrf_token"] != request.form["csrf_token"]):
            return abort(403)
        new_username = request.form["new_username"]
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
        if (session["csrf_token"] != request.form["csrf_token"]):
            return abort(403)
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
        if (password != request.form["password_validation"]):
            print("INCORRECT VALIDATION")
            return render_template("sign_up.html", error=True, message="Salasanat eivät täsmää")
        if (users.sign_up(username, password)):
            return render_template("log_in.html", success=True, message="Käyttäjätunnus luotu, kirjaudu sisään", new_user=True)
        else:
            print("USERNAME TAKEN")
            return render_template("sign_up.html", error=True, message="Käyttäjätunnus varattu")


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "GET":
        return render_template("report.html")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        utils.add_report(title, content)
        return render_template("report.html", message="Kiitos viestistäsi")

# events
@app.route("/event/<int:id>")
def event(id):
    event = utils.event_to_dictionary(events.get_event_by_id(id))
    description_split = event["description"].splitlines()
    image_id = event["image_id"]
    return render_template("event.html", event=event, image_id=image_id, description_split=description_split)


@app.route("/event_image/<int:id>")
def event_image(id):
    image = utils.get_image_data(id)
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response


@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    if request.method == "GET":
        if (session["suspended"]):
            return "<h1>SUSPENDED ACCOUNT, NO ACCESS</h1>"
        categories = utils.get_categories()
        counties = utils.get_counties()
        return render_template("create_event.html", categories=categories, counties=counties)

    if request.method == "POST":
        if (session["csrf_token"] != request.form["csrf_token"]):
            return abort(403)
        event_name = request.form["event_name"]
        category_id = utils.get_category_id(request.form["category"])
        description = request.form["description"]
        print("DESCRIPTION", description)
        cost = request.form["cost"]
        if (cost == "free"):
            price = "Ilmainen"
        else:
            price = request.form["price"]
            if not "€" in price:
                price = price + "€"
        county_id = utils.get_county_id(request.form["county"])
        city = request.form["city"]
        locale = request.form["locale"]
        address = request.form["address"]
        starting_time = request.form["starting_time"]
        ending_time = request.form["ending_time"]
        # handle image
        image = request.files["image"]
        if (image):
            image_name = image.filename
            data = image.read()
            image_id = utils.add_image_and_return_id(image_name, data)

            events.add_event_with_image(
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
        else:
            events.add_event_without_image(
                event_name,
                category_id,
                description,
                price,
                county_id,
                city,
                locale,
                address,
                starting_time,
                ending_time
            )
        return redirect("/")


@app.route("/edit_event/<int:id>", methods=["GET", "POST"])
def edit_event(id):
    if request.method == "GET":
        if session["suspended"]:
            return "<h1>SUSPENDED ACCOUNT, NO ACCESS</h1>"
        event = events.get_event_by_id(id)
        creator = users.get_username(event[2])
        if session["username"] != creator and not session["is_admin"]:
            return "No access"
        event_category = utils.get_category_name(event[3])
        event_county = utils.get_county_name(event[4])
        categories = utils.get_categories()
        counties = utils.get_counties()
        starting_time = utils.timestamp_to_datetime(event[-4])
        ending_time = utils.timestamp_to_datetime(event[-3])

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
        if (session["csrf_token"] != request.form["csrf_token"]):
            return abort(403)
        event_name = request.form["event_name"]
        category_id = utils.get_category_id(request.form["category"])
        description = request.form["description"]
        cost = request.form["cost"]
        if (cost == "free"):
            price = "Ilmainen"
        else:
            price = request.form["price"]
            if not "€" in price:
                price = price + "€"
        county_id = utils.get_county_id(request.form["county"])
        city = request.form["city"]
        locale = request.form["locale"]
        address = request.form["address"]
        starting_time = request.form["starting_time"]
        ending_time = request.form["ending_time"]

        # handle image
        image = request.files["image"]
        if (image):
            image_name = image.filename
            data = image.read()
            image_id = utils.add_image_and_return_id(image_name, data)

            events.edit_event_with_image(
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
                image_id
            )
        else:
            events.edit_event_without_image(
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
                ending_time
            )

        return redirect("/user_info")


@app.route("/delete_event/<int:id>", methods=["GET", "POST"])
def delete_event(id):
    print("WE IN DELETE")
    event = events.get_event_by_id(id)
    creator = users.get_username(event[2])
    if session["username"] != creator and not session["is_admin"]:
        return "No access"
    image_id = events.get_image_id(id)
    events.delete_event(id)
    if (image_id):
        utils.delete_image(image_id)
    if users.session["is_admin"]:
        return redirect("/admin_page")
    else:
        return redirect("/user_info")

# admin


@app.route("/admin_page")
def admin_page():
    if not users.session["is_admin"]:
        return "No access"
    else:
        usernames = users.get_all_users_id_username_suspend()
        all_events = utils.events_to_dictionaries(events.get_all())
        reports = utils.get_reports()
        user_count = users.get_user_count()
        event_count = events.get_event_count()
        return render_template("admin_page.html", usernames=usernames, events=all_events, reports=reports, user_count=user_count, event_count=event_count)


@app.route("/mark_as_read_report/<int:id>")
def mark_as_read_report(id):
    utils.mark_as_read_report(id)
    return redirect("/admin_page")


@app.route("/delete_report/<int:id>")
def delete_report(id):
    utils.delete_report(id)
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
    users_events = events.get_events_by_user_id(id)
    image_ids = []
    for event in users_events:
        # delete images
        event_image_id = events.get_image_id(event[0])
        if (event_image_id):
            image_ids.append(event_image_id)
        events.delete_event(event[0])
    for image_id in image_ids:
        utils.delete_image(image_id)
    if (users.session["is_admin"]):
        users.delete(id)
        return redirect("/admin_page")
    else:
        users.log_out()
        users.delete(id)
        return redirect("/")
