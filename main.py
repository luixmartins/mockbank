import sqlite3 

connection = sqlite3.connect('db.sqlite3')

with connection as conn: 
    cursor = conn.cursor() 

    response = cursor.execute("delete from user_user where owner_id = 13")

print(response)
