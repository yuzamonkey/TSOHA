from db import db
import users
import attributes


def get_all():
    sql_response = db.session.execute("SELECT * FROM Events ORDER BY Starting_time").fetchall()
    return sql_response

def get_event_by_id(id):
    sql = "SELECT * FROM Events WHERE id=:id"
    event = db.session.execute(sql, {"id":id}).fetchone()
    return event

def get_events_by_user_id(user_id):
    sql = "SELECT * FROM Events WHERE user_id=:user_id"
    events = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return events

def get_image_id(event_id):
    sql = "SELECT image_id FROM Events WHERE id=:event_id"
    image_id = db.session.execute(sql, {"event_id":event_id}).fetchone()[0]
    return image_id

def add_event(name, category_id, description, price, county_id, city, locale, address, starting_time, ending_time, image_id):
    starting_time = attributes.format_date(starting_time)
    ending_time = attributes.format_date(ending_time)
    sql = """
        INSERT INTO Events (
            name, 
            user_id,
            category_id, 
            description, 
            price, 
            county_id, 
            city, 
            locale, 
            address, 
            starting_time, 
            ending_time,
            image_id) values (
                :name,
                :user_id,
                :category_id,
                :description,
                :price,
                :county_id,
                :city,
                :locale,
                :address,
                :starting_time,
                :ending_time,
                :image_id
                )"""
    db.session.execute(sql, {
        "name":name, 
        "user_id":users.session["user_id"],
        "category_id":category_id,
        "description":description,
        "price":price,
        "county_id":county_id,
        "city":city,
        "locale":locale,
        "address":address,
        "starting_time":starting_time,
        "ending_time":ending_time,
        "image_id":image_id
        })
    db.session.commit()
