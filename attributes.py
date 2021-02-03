from db import db

def get_counties():
    sql_counties = db.session.execute("SELECT County FROM Counties ORDER BY County").fetchall()
    counties = []
    for county in sql_counties:
        counties.append(str(county)[2:-3])
    return counties