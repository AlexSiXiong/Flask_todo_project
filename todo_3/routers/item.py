import sqlite3
import sys
sys.path.append('..')
from fastapi import APIRouter, Depends, Request, Form
from todo_3.routers.user import decode_cur_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from starlette.responses import RedirectResponse
from starlette import status

db_name = 'todo.db'
table_name = 'todo'

router = APIRouter(prefix="/todo_list",
    tags=["items"])

templates = Jinja2Templates('templates')

# @router.get('/test', response_class=HTMLResponse)
# async def test_html(request: Request):
#     return templates.TemplateResponse('register.html', {"request":request})

# @router.get("/")
# async def get_all():
#     connection = sqlite3.connect(db_name)
#     cursor = connection.cursor()

#     query_script = "SELECT * FROM {}".format(table_name)
#     result = cursor.execute(query_script)

#     res = result.fetchall()
#     connection.close()

#     if res:
#         return res
#     return {'msg': 'no info'}, 404

# @router.get("/todo/login")
# async def get_all_items_by_user(user=Depends(decode_cur_user)):
#     if user is None:
#         return {'msg': 'cannot login'}
#     user_id = user['user_id']

#     connection = sqlite3.connect(db_name)
#     cursor = connection.cursor()

#     query_script = "SELECT * FROM {} where owner={}".format(table_name, user_id)
#     result = cursor.execute(query_script)

#     res = result.fetchall()
#     connection.close()
#     if res:
#         return res
#     return {'msg': 'no info'}, 404


# @router.get("/todo/login/{item_id}")
# async def get_one_item_by_user(item_id, user=Depends(decode_cur_user)):
#     if user is None:
#         return {'msg': 'cannot login'}
#     user_id = user['user_id']

#     connection = sqlite3.connect(db_name)
#     cursor = connection.cursor()

#     query_script = "SELECT * FROM {} where owner={} and id={}".format(table_name, user_id, item_id)
#     result = cursor.execute(query_script)

#     res = result.fetchone()
#     connection.close()
#     if res:
#         return res
#     return {'msg': 'no info'}, 404


# @router.delete("/todo/delete/{id}")
# async def delete_item_by_id3(id, user=Depends(decode_cur_user)):
#     if user is None:
#         return {'msg': 'cannot login'}

#     connection = sqlite3.connect(db_name)
#     cursor = connection.cursor()
#     # find item by id
#     # query = "UPDATE {} SET display=0 WHERE id=? and onwer=?".format(table_name)
#     query = "DELETE FROM {} WHERE id=?".format(table_name)
#     cursor.execute(query, (id))

#     connection.commit()
#     connection.close()
    
#     return {'msg': 'item id {} removed'.format(id)}


# @router.get("/get/{item_id}")
# async def get_item_by_id(item_id):
#     connection = sqlite3.connect(db_name)
#     cursor = connection.cursor()

#     query_script = "SELECT * FROM {} where id={}".format(table_name, item_id)
#     result = cursor.execute(query_script)

#     res = result.fetchall()
#     connection.close()

#     if res:
#         return res
#     else:
#         return {'msg': 'item id not exists'}

# @router.post("/post/")
# async def post_item(name, description, priority, user=Depends(decode_cur_user)):
#     """
#     (
#         id INTEGER PRIMARY KEY, 
#         item text, 
#         description text,
#         priority integer,
#         complete boolean defult 0,
#         display boolean default 1
#     )
    
#     """
#     if user is None:
#         return {'msg': 'cannot login'}
#     user_id = user['user_id']

#     connection = sqlite3.connect(db_name)
#     cursor = connection.cursor()

#     # Todo: this is not the best practice, I set the DEFAULT values of two cols manully
#     query_script = "INSERT INTO {} VALUES(?,?,?,?,?,0,1)".format(table_name) 
#     cursor.execute(query_script, (None, name, description, priority, user_id))

#     connection.commit()
#     connection.close()
    
#     return {'msg': '{} description:{} priority:{} added'.format(name, description, priority)}

# @router.post("/delete/{id}")
# async def delete_item_by_id(id):
#     connection = sqlite3.connect(db_name)
#     cursor = connection.cursor()
#     # find item by id
#     query = "UPDATE {} SET display=0 WHERE id=?".format(table_name)
#     cursor.execute(query, (id,))

#     connection.commit()
#     connection.close()
    
#     return {'msg': 'item id {} removed'.format(id)}

# @router.delete("/delete2/{id}")
# async def delete_item_by_id2(id):
#     connection = sqlite3.connect(db_name)
#     cursor = connection.cursor()
#     # find item by id
#     query = "DELETE FROM {} WHERE id=?".format(table_name)
#     cursor.execute(query, (id,))

#     connection.commit()
#     connection.close()
    
#     return {'msg': 'item id {} removed'.format(id)}

@router.get("/", response_class=HTMLResponse)
async def get_all_items(request: Request):
    user = await decode_cur_user(request)
    if user is None:
        return RedirectResponse(url='/user')
    user_id = user['user_id']
    

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    query_script = "SELECT * FROM {} where owner={}".format(table_name, user_id)
    result = cursor.execute(query_script)
    res = result.fetchall()
    connection.close()

    return templates.TemplateResponse("index.html", {"request": request, "items": res, "user_name":user['user_name']})

@router.get("/add_item", response_class=HTMLResponse)
async def add_an_item(request: Request):
    user = await decode_cur_user(request)
    if user is None:
        return RedirectResponse(url='/user')
    return templates.TemplateResponse("add_item.html", {"request": request, "user_name":user['user_name']})

@router.post("/add_item", response_class=HTMLResponse)
async def add_an_item(request: Request,
                        item_name:str=Form(...), 
                        description=Form(...), 
                        priority=Form(...)):
    # use Form(...) or cannot accept parameters passed
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
    user = await decode_cur_user(request)
    if user is None:
        return RedirectResponse(url='/user')
    user_id = user['user_id']

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Todo: this is not the best practice, I set the DEFAULT values of two cols manully
    query_script = "INSERT INTO {} VALUES(?,?,?,?,?,0,1)".format(table_name) 
    cursor.execute(query_script, (None, item_name, description, priority, user_id))

    connection.commit()
    connection.close()
    return RedirectResponse(url='/todo_list/', status_code=status.HTTP_302_FOUND)

@router.get("/complete/{item_id}", response_class=HTMLResponse)
async def complete_todo(request: Request, item_id):
    user = await decode_cur_user(request)
    if user is None:
        return RedirectResponse(url='/user')

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    query_script = "SELECT * FROM {} where id={}".format(table_name, item_id)
    result = cursor.execute(query_script)
    res = result.fetchone()

    complete_status = res[5]
    complete_status = 0 if complete_status else 1

    query_script = "UPDATE {} SET complete={} WHERE id={}".format(table_name, complete_status, item_id)
    cursor.execute(query_script)

    connection.commit()
    connection.close()

    return RedirectResponse(url='/todo_list')



@router.get("/delete/{item_id}")
async def delete_item(request: Request, item_id):
    user = await decode_cur_user(request)
    if user is None:
        return RedirectResponse(url='/user')

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # find item by id
    query = "DELETE FROM {} WHERE id=?".format(table_name)
    cursor.execute(query, (item_id,))

    connection.commit()
    connection.close()
    return RedirectResponse(url='/todo_list')


