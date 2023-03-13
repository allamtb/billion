import datetime

# Access DB absolute file path
from billions.util.Accdb import Accdb

path = r"F:\billionsData\kong.com.accdb"

# You can use Accdb.convert_date(dt) to convert datetime to Access format
# qry_insert = f"INSERT INTO my_first_table (item, dt) VALUES ('New Item', {accdb.Accdb.convert_date(datetime.datetime.now())});"
qry_select = "SELECT * FROM inews;"

# Classic way
db = Accdb(path)
db.execute(qry_select)
print(db.query(qry_select))

# # Using with statement
# with Accdb(path) as db:
#
#     print(db.query(qry_select))