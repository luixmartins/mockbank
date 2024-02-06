import sqlite3 

try: 
    connection = sqlite3.connect('db.sqlite3')
    with connection as conn: 
        cursor = conn.cursor() 

        response = cursor.execute("delete from service_transfermodel where sent_by_id = 13")
except: 
    print('Não conectado')



print(response)
