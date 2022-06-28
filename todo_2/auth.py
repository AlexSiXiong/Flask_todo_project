from fastapi import FastAPI
import sqlite3

app = FastAPI()

db_name = 'todo.db'
table_name = 'user'

@app.get("/")
async def enter():
    return {'msg': 'hello world'}, 200

@app.post('/create/user')
async def create_user(username, password):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Todo: this is not the best practice, I set the DEFAULT values of two cols manully
    query_script = "INSERT INTO {} VALUES(?,?,?,1)".format(table_name) 
    cursor.execute(query_script, (None, username, password))

    connection.commit()
    connection.close()
    
    return {'msg': 'user:{} ; pwd:{}  added'.format(username, password)}