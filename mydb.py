import MySQLdb

# create database connection
db = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='', # I have no password set for this db
)

# prepare a cursor object
cursorObject = db.cursor()

# create a database
cursorObject.execute("CREATE DATABASE IF NOT EXISTS elderco")

print("Database was created!")