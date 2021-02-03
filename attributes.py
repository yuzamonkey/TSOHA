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

