from fastapi import FastAPI, Depends
import sqlite3
from auth import decode_cur_user
import logging
# http://127.0.0.1:3001/post/?name=coding&description=java&priority=1


app = FastAPI()
db_name = 'todo.db'
table_name = 'todo'

@app.get("/")
async def get_all():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    query_script = "SELECT * FROM {}".format(table_name)
    result = cursor.execute(query_script)

    res = result.fetchall()
    connection.close()

    if res:
        return res
    return {'msg': 'no info'}, 404

@app.get("/todo/login")
async def get_all_items_by_user(user=Depends(decode_cur_user)):
    if user is None:
        return {'msg': 'cannot login'}
    user_id = user['user_id']

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    query_script = "SELECT * FROM {} where owner={}".format(table_name, user_id)
    result = cursor.execute(query_script)

    res = result.fetchall()
    connection.close()
    if res:
        return res
    return {'msg': 'no info'}, 404


@app.get("/todo/login/{item_id}")
async def get_one_item_by_user(item_id, user=Depends(decode_cur_user)):
    if user is None:
        return {'msg': 'cannot login'}
    user_id = user['user_id']

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    query_script = "SELECT * FROM {} where owner={} and id={}".format(table_name, user_id, item_id)
    result = cursor.execute(query_script)

    res = result.fetchone()
    connection.close()
    if res:
        return res
    return {'msg': 'no info'}, 404


@app.delete("/todo/delete/{id}")
async def delete_item_by_id3(id, user=Depends(decode_cur_user)):
    if user is None:
        return {'msg': 'cannot login'}

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # find item by id
    # query = "UPDATE {} SET display=0 WHERE id=? and onwer=?".format(table_name)
    query = "DELETE FROM {} WHERE id=?".format(table_name)
    cursor.execute(query, (id))

    connection.commit()
    connection.close()
    
    return {'msg': 'item id {} removed'.format(id)}


@app.get("/get/{item_id}")
async def get_item_by_id(item_id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    query_script = "SELECT * FROM {} where id={}".format(table_name, item_id)
    result = cursor.execute(query_script)

    res = result.fetchall()
    connection.close()

    if res:
        return res
    else:
        return {'msg': 'item id not exists'}

@app.post("/post/")
async def post_item(name, description, priority, user=Depends(decode_cur_user)):
    """
    (
        id INTEGER PRIMARY KEY, 
        item text, 
        description text,
        priority integer,
        complete boolean defult 0,
        display boolean default 1
    )
    
    """
    if user is None:
        return {'msg': 'cannot login'}
    user_id = user['user_id']

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Todo: this is not the best practice, I set the DEFAULT values of two cols manully
    query_script = "INSERT INTO {} VALUES(?,?,?,?,?,0,1)".format(table_name) 
    cursor.execute(query_script, (None, name, description, priority, user_id))

    connection.commit()
    connection.close()
    
    return {'msg': '{} description:{} priority:{} added'.format(name, description, priority)}

@app.post("/delete/{id}")
async def delete_item_by_id(id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # find item by id
    query = "UPDATE {} SET display=0 WHERE id=?".format(table_name)
    cursor.execute(query, (id,))

    connection.commit()
    connection.close()
    
    return {'msg': 'item id {} removed'.format(id)}

@app.delete("/delete2/{id}")
async def delete_item_by_id2(id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # find item by id
    query = "DELETE FROM {} WHERE id=?".format(table_name)
    cursor.execute(query, (id,))

    connection.commit()
    connection.close()
    
    return {'msg': 'item id {} removed'.format(id)}