from db import db


def format_date(date_result):
    date = date_result[:10]
    time = date_result[-5:]
    formatted_date = date + " " + time
    return formatted_date

def get_all():
    sql_response = db.session.execute("SELECT * FROM Events ORDER BY Starting_time").fetchall()
    return sql_response
    
def add_event(name, category_id, description, price, county_id, city, locale, address, starting_time, ending_time, image_id):
    starting_time = format_date(starting_time)
    ending_time = format_date(ending_time)
    #add user_id
    sql = f"""
        INSERT INTO Events (
            name, 
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
                '{name}',
                {category_id},
                '{description}',
                '{price}',
                {county_id},
                '{city}',
                '{locale}',
                '{address}',
                '{starting_time}',
                '{ending_time}',
                {image_id}
                )"""
    db.session.execute(sql)
    db.session.commit()
