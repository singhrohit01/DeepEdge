
from workload import Workload
from helpers.db_connector import Connection
from helpers.util import read_JSON,format_time
import datetime

workload = Workload()
config = read_JSON("config.json")

cursor = []

# read all data from local database
db_credentials = config["credentials"]["database"]["local"]
with Connection(db_credentials["host"], db_credentials["username"], db_credentials["password"], db_credentials["db"]) as db_connection:
    cursor = db_connection.execute_query("SELECT * FROM runs")

# the data retrieved needs a little bit of formatting before pushing to the server
rows = []
for row in cursor :
    values = []
    for each_value in row :
        if isinstance(each_value, datetime.datetime):
            values.append("'{}'".format(format_time(each_value)))
        else:
            values.append(str(each_value))
    rows.append(",".join(values))

# push it to server (duplicates are handled using unique keys)
db_credentials = config["credentials"]["database"]["cloud"]
with Connection(db_credentials["host"], db_credentials["username"], db_credentials["password"], db_credentials["db"]) as db_connection:
    
    for row in cursor:
        query = "INSERT INTO runs VALUES({}) ON DUPLICATE KEY UPDATE id=id".format(row)

        db_connection.execute_query(query)
    
    db_connection.commit()

