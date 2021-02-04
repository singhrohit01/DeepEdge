#!/usr/bin/python
import os.path as path
from helpers.db_connector import Connection
from helpers.util import read_JSON

def upsertFromFile(con, filename, table):
    """
        Helper method that takes in a filename which should be a json 
        and inserts(or updates if data already exists) the data from the file into the table specified
    """
    items = read_JSON(filename)

    for item in items:
        values = "0,"   # the id field; it's an auto-increment field but have to include in the query to match column count
        for attr in item:
            values += "\"{}\",".format(item[attr])
        values = values[:len(values) - 1]   # remove the last comma
        con.execute_query("INSERT INTO {table} values({values}) ON DUPLICATE KEY UPDATE id=id".format_map({ "table" : table, "values" : values }))
    
    print("{} rows ready for upsertion for {}".format(len(items), table))

config = read_JSON('config.json')

db_credentials = config["credentials"]["database"][config["db_provider"]]

con = Connection(db_credentials['host'], db_credentials['username'], db_credentials['password'], db_credentials['db'])

con.connect()

# Currently, we are storing all the initial info in a json file
# then reading it here and inserting/upserting it in the database
# This makes the json file easier to read and manage

# There is a more efficient way (in terms of computation) though
# Check out https://dev.mysql.com/doc/refman/8.0/en/load-data.html
# We can directly load a file to the table

# load devices
baseDir = "data"
upsertFromFile(con, path.join(baseDir, "devices.json"), "devices")
upsertFromFile(con, path.join(baseDir, "frameworks.json"), "frameworks")
upsertFromFile(con, path.join(baseDir, "models.json"), "models")
upsertFromFile(con, path.join(baseDir, "applications.json"), "applications")

con.commit()

print("done")