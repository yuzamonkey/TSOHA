from db import db

def result_to_array(response):
    array = []
    for item in response:
        array.append(str(item)[2:-3])
    return array

def get_counties():
    sql_response = db.session.execute("SELECT County FROM Counties ORDER BY County").fetchall()
    return result_to_array(sql_response)

def get_categories():
    sql_response = db.session.execute("SELECT Category FROM Categories ORDER BY Category").fetchall()
    return result_to_array(sql_response)
