from fastapi import FastAPI
import sqlite3

app = FastAPI()

db_name = 'todo.db'
table_name = 'user'

@app.get("/")
async def enter():
    return {'msg': 'hello world'}, 200

@app.post("/login")
async def verify_user(new_username, new_password):
    connection = sqlite3.connect('todo.db')

    cursor = connection.cursor()

    sql_script = "select password from {} where name='{}'".format(db_name, new_username)
    res = cursor.execute(sql_script)
    save_password = res.fetchone()
    connection.close()

    if save_password:
        save_password = save_password[0]
    if save_password == new_password:
        return {'msg': 'user login'}

    return {'msg': 'user not exist or wrong password'}

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