__author__ = 'workhorse'

import sqlite3 as lite
import pandas as pd


con = lite.connect('cities.db')
with con:
    cur = con.cursor()
    cur.execute("drop table if exists cities")
    cur.execute("drop table if exists weather")
    cur.execute("drop TABLE if EXISTS cities_copy")
    cur.execute("CREATE TABLE cities(name TEXT, state TEXT)")
    cur.execute("CREATE TABLE weather(city TEXT, year INTEGER , warm_month TEXT, cold_month TEXT, average_high INTEGER)")




cities = (
    ('New York City', 'NY'),
    ('Boston', 'MA'),
    ('Chicago', 'IL'),
    ('Miami', 'FL'),
    ('Dallas', 'TX'),
    ('Seattle', 'WA'),
    ('Portland', 'OR'),
    ('San Francisco', 'CA'),
    ('Los Angeles', 'CA'),
    ('Washington', 'DC'),
    ('Houston', 'TX'),
    ('Las Vegas', 'NV'),
    ('Atlanta', 'GA')
)

weather = (
    ('New York City', 2013, 'July', 'January', 62),
    ('Boston',  2013,   'July',   'January', 59),
    ('Chicago', 2013,   'July', 'January',59),
    ('Miami',2013,'August','January',84),
    ('Dallas',2013,'July','January',77),
    ('Seattle',2013,'July','January', 61),
    ('Portland',2013,'July','December',63),
    ('San Francisco',2013,'September','December',64),
    ('Los Angeles',2013,'September','December',75),
    ('Washington', 2013, 'July', 'January', 55),
    ('Houston', 2013, 'July', 'January',56),
    ('Las Vegas',2013,'July','December', 77),
    ('Atlanta', 2013, 'July', 'January', 96)
)



con = lite.connect('cities.db')
with con:
    cur = con.cursor()
    cur.executemany("INSERT INTO cities VALUES(?,?)", cities)
    cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)


with con:
    #compared iterating across rows vs a dataframe
    cur = con.cursor()
    cur.execute("SELECT name, state, year, warm_month, cold_month, average_high \
                FROM cities INNER JOIN weather WHERE name = city;")
    rows = cur.fetchall()
    #printed cur.descriptions so I could see the headers
    print cur.description
    #named the columns from descriptions to avoid having to use index numbers
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=cols)
    print df


    cur.execute("SELECT city, state, average_high, warm_month \
                FROM weather \
                Inner join cities\
                WHERE city = name AND warm_month ='July';")
    rows = cur.fetchall()
    print"Iterating via rows - The cities that are warmest in July are:"
    for row in rows:
        print row[0]
    print"Iterating across dataframe - The cities that are warmest in July are:"
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=cols)
    for city in (df['city']):
        print city
        #testing formating strings
        print "{} is my favorite city". format(city)


"""
Question - how do do I iterate across dataframe properly
"""