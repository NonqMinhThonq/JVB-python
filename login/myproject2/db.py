import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'minhthon9'
)

# prepaer a cursor object
cursorObject = database.cursor()

# create a database 
cursorObject.execute('create database users2')