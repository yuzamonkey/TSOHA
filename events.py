from db import db
import users
import attributes


def get_all():
    all_events = db.session.execute("SELECT * FROM Events ORDER BY Starting_time").fetchall()
    return all_events

def get_all_filter_by_category(category_id):
    sql = "SELECT * FROM Events WHERE category_id=:category_id ORDER BY Starting_time"
    events = db.session.execute(sql, {"category_id":category_id})
    return events

def get_all_filter_by_county(county_id):
    sql = "SELECT * FROM Events WHERE county_id=:county_id ORDER BY Starting_time"
    events = db.session.execute(sql, {"county_id":county_id})
    return events

def get_all_filter_by_category_and_county(category_id, county_id):
    sql = "SELECT * FROM Events WHERE category_id=:category_id and county_id=:county_id ORDER BY Starting_time"
    events = events = db.session.execute(sql, {"category_id":category_id,"county_id":county_id})
    return events

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

def add_event_with_image(name, category_id, description, price, county_id, city, locale, address, starting_time, ending_time, image_id):
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

def add_event_without_image(name, category_id, description, price, county_id, city, locale, address, starting_time, ending_time):
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
            ending_time) values (
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
                :ending_time
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
        "ending_time":ending_time
        })
    db.session.commit()

def edit_event_with_image(id, name, category_id, description, price, county_id, city, locale, address, starting_time, ending_time, image_id):
    starting_time = attributes.format_date(starting_time)
    ending_time = attributes.format_date(ending_time)
    sql = """UPDATE Events SET 
        name=:name, 
        category_id=:category_id, 
        description=:description,
        price=:price, 
        county_id=:county_id, 
        city=:city, 
        locale=:locale, 
        address=:address, 
        starting_time=:starting_time, 
        ending_time=:ending_time,
        image_id=:image_id       
        WHERE id=:id"""

    db.session.execute(sql, {
        "name":name,
        "category_id":category_id,
        "description":description,
        "price":price,
        "county_id":county_id,
        "city":city,
        "locale":locale,
        "address":address,
        "starting_time":starting_time,
        "ending_time":ending_time,
        "image_id":image_id,
        "id":id
    })
    db.session.commit()

def edit_event_without_image(id, name, category_id, description, price, county_id, city, locale, address, starting_time, ending_time):
    starting_time = attributes.format_date(starting_time)
    ending_time = attributes.format_date(ending_time)
    sql = """UPDATE Events SET 
        name=:name, 
        category_id=:category_id, 
        description=:description,
        price=:price, 
        county_id=:county_id, 
        city=:city, 
        locale=:locale, 
        address=:address, 
        starting_time=:starting_time, 
        ending_time=:ending_time    
        WHERE id=:id"""

    db.session.execute(sql, {
        "name":name,
        "category_id":category_id,
        "description":description,
        "price":price,
        "county_id":county_id,
        "city":city,
        "locale":locale,
        "address":address,
        "starting_time":starting_time,
        "ending_time":ending_time,
        "id":id
    })
    db.session.commit()

def delete_event(id):
    #get image_id
    img_sql = "SELECT image_id FROM Events WHERE id=:id"
    img_id = db.session.execute(img_sql, {"id":id}).fetchone()[0]
    #delete event
    sql = "DELETE FROM Events WHERE id=:id"
    db.session.execute(sql, {"id":id})
    #delete events image
    if (img_id):
        delete_img_sql = "DELETE FROM Images WHERE id=:id"
        db.session.execute(delete_img_sql, {"id":img_id})
    db.session.commit()

def get_event_count():
    sql = "SELECT COUNT(*) FROM Events"
    count = db.session.execute(sql).fetchone()[0]
    return count


