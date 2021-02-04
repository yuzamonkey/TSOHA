from db import db

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
    category_id = db.session.execute(f"SELECT id FROM Categories WHERE Category='{category_name}'").fetchone()[0]
    return int(category_id)

def get_county_id(county_name):
    county_id = db.session.execute(f"SELECT id FROM Counties WHERE County='{county_name}'").fetchone()[0]
    return int(county_id)

def get_image_data(id):
    image_data = db.session.execute(f"SELECT data FROM images WHERE id={id}").fetchone()[0]
    return image_data

def add_image_and_return_id(name, data):
    sql = "INSERT INTO images (name,data) VALUES (:name,:data) RETURNING id"
    id = db.session.execute(sql, {"name":name,"data":data}).fetchone()[0]
    db.session.commit()
    return id