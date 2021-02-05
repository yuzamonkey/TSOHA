from db import db

def format_date(date_result):
    date = date_result[:10]
    time = date_result[-5:]
    formatted_date = date + " " + time
    return formatted_date

def timestamp_to_datetime(timestamp):
    date = str(timestamp)[:10]
    time = str(timestamp)[11:16]
    return f"{date}T{time}"


def result_to_array(response):
    array = []
    for item in response:
        array.append(str(item)[2:-3])
    return array


def get_categories():
    sql_response = db.session.execute("SELECT Category FROM Categories ORDER BY Category").fetchall()
    return result_to_array(sql_response)

def get_counties():
    sql_response = db.session.execute("SELECT County FROM Counties ORDER BY County").fetchall()
    return result_to_array(sql_response)

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