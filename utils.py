from db import db
import users

def datetime_to_timestamp(date_result):
    date = date_result[:10]
    time = date_result[-5:]
    formatted_date = date + " " + time
    return formatted_date

def timestamp_to_datetime(timestamp):
    date = str(timestamp)[:10]
    time = str(timestamp)[11:16]
    return f"{date}T{time}"

def timestamp_to_dmyhm(timestamp):
    year = str(timestamp)[:4] 
    month = str(timestamp)[5:7]
    day = str(timestamp)[8:10]
    hours = str(timestamp)[11:13]
    minutes = str(timestamp)[14:16]
    ddmmyyyyhhmm = f"{day}.{month}.{year} {hours}:{minutes}"
    return ddmmyyyyhhmm

def event_to_dictionary(event):
    dictionary = {
            "id": event[0],
            "name": event[1],
            "creator": users.get_username(event[2]),
            "category": get_category_name(event[3]),
            "county": get_county_name(event[4]),
            "locale": event[5],
            "city": event[6],
            "address": event[7],
            "description": event[8],
            "starting_time": timestamp_to_dmyhm(event[9]),
            "ending_time": timestamp_to_dmyhm(event[10]),
            "price": event[11],
            "image_id": event[12]
        }
    return dictionary

def events_to_dictionaries(events):
    all_events = []
    for event in events:
        all_events.append(event_to_dictionary(event))
    return all_events

def result_to_array(response):
    array = []
    for item in response:
        array.append(str(item)[2:-3])
    return array

def get_categories():
    categories = db.session.execute("SELECT Category FROM Categories ORDER BY Category").fetchall()
    return result_to_array(categories)

def get_counties():
    counties = db.session.execute("SELECT County FROM Counties ORDER BY County").fetchall()
    return result_to_array(counties)

def get_category_id(category_name):
    sql = "SELECT id FROM Categories WHERE Category=:category_name"
    category_id = db.session.execute(sql, {"category_name":category_name}).fetchone()[0]
    return int(category_id)

def get_county_id(county_name):
    sql = "SELECT id FROM Counties WHERE County=:county_name"
    county_id = db.session.execute(sql, {"county_name":county_name}).fetchone()[0]
    return int(county_id)

def get_category_name(id):
    sql = "SELECT Category FROM Categories WHERE id=:id"
    category = db.session.execute(sql, {"id":id}).fetchone()[0]
    return category

def get_county_name(id):
    sql = "SELECT County FROM Counties WHERE id=:id"
    county = db.session.execute(sql, {"id":id}).fetchone()[0]
    return county

def get_image_data(id):
    sql = "SELECT data FROM images WHERE id=:id"
    image_data = db.session.execute(sql, {"id":id}).fetchone()[0]
    return image_data

def add_image_and_return_id(name, data):
    sql = "INSERT INTO images (name,data) VALUES (:name,:data) RETURNING id"
    id = db.session.execute(sql, {"name":name,"data":data}).fetchone()[0]
    db.session.commit()
    return id

def add_report(title, content):
    sql = f"INSERT INTO Reports (title, content, unread)VALUES (:title, :content, {True})"
    db.session.execute(sql, {"title":title, "content":content})
    db.session.commit()

def get_reports():
    sql = "SELECT * FROM Reports ORDER BY id DESC"
    reports = db.session.execute(sql).fetchall()
    return reports

def mark_as_read_report(id):
    sql = f"UPDATE Reports SET Unread={False} WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def delete_report(id):
    sql = "DELETE FROM Reports WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
