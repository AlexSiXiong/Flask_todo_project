from datetime import datetime, timedelta
from http.client import HTTPException
from pickletools import StackObject
from telnetlib import STATUS
from tempfile import TemporaryFile
from fastapi import Depends, APIRouter, Request, Response, Form
import sqlite3

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import sys
sys.path.append('..')

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from starlette.responses import RedirectResponse

templates = Jinja2Templates('templates')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/user",
    tags=["user"])

db_name = 'todo.db'
table_name = 'user'

class LoginForm:
    def __init__(self, request:Request) -> None:
        self.request = request
        self.user_name = None
        self.password = None
    
    async def create_oauth_form(self):
        form = await self.request.form()
        self.user_name = form.get('username')
        self.password = form.get('password')


@router.post("/login")
async def verify_user(new_username, new_password):
    connection = sqlite3.connect(db_name)

    cursor = connection.cursor()

    sql_script = "select id, password from {} where name='{}'".format(table_name, new_username)
    res = cursor.execute(sql_script)
    query_res = res.fetchone()
    connection.close()

    if not query_res:
        return {'msg': 'user not exist or wrong password'}

    id = query_res[0]
    save_password = query_res[1]

    if save_password == new_password:
        token = create_access_token(new_username, id)
        return {'msg': 'user login', 'token': token}
    return {'msg': 'user not exist or wrong password'}


async def decode_cur_user(request:Request):
    try:
        cur_token = request.cookies.get("access_token")
        if cur_token is None:
            return None
        payload = jwt.decode(cur_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name = payload.get('sub')
        user_id = payload.get('id')
        if user_name is None or user_id is None:
            return None
        return {
            "user_name": user_name,
            "user_id": user_id
        }
    except JWTError:
        raise HTTPException(STATUS=404, detail='JWT error')

def create_access_token(user_name, user_id):
    expire_time = datetime.utcnow() + timedelta(735) # expire 15 min
    
    encode = {
        "sub": user_name, 
        "id": user_id,
        "exp": expire_time
    }

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
@router.post('/create')
async def create_user(username, password):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Todo: this is not the best practice, I set the DEFAULT values of two cols manully
    query_script = "INSERT INTO {} VALUES(?,?,?,1)".format(table_name) 
    cursor.execute(query_script, (None, username, password))

    connection.commit()
    connection.close()
    
    return {'msg': 'user:{} ; pwd:{}  added'.format(username, password)}


@router.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('login.html', {"request":request})

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse('register.html', {"request":request})

@router.post('/', response_class=HTMLResponse)
async def login(request: Request):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url='/todo_list', status_code=302)

        validate_user_cookie = await verify_user(response=response, 
        new_username=form.user_name, 
        new_password=form.password)

        if not validate_user_cookie:
            return templates.TemplateResponse('login.html',
            {"request": request, "msg": "incorrect username or password"})
        return response
    except HTTPException:
         return templates.TemplateResponse('login.html',
         {"request":request, "msg": "try again"})


@router.post("/login")
async def verify_user(response: Response, new_username, new_password):
    connection = sqlite3.connect(db_name)

    cursor = connection.cursor()

    sql_script = "select id, password from {} where name='{}'".format(table_name, new_username)
    res = cursor.execute(sql_script)
    query_res = res.fetchone()
    connection.close()

    if not query_res:
        return False

    id = query_res[0]
    save_password = query_res[1]

    if save_password == new_password:
        token = create_access_token(new_username, id)
        response.set_cookie(key='access_token', value=token, httponly=True)
        return True

    return False


@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response

@router.get("/add_user", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse('register.html', {"request":request})

@router.post("/add_user", response_class=HTMLResponse)
async def register(request: Request,
                   username:str=Form(...),
                   password:str=Form(...),
                   valid_password:str=Form(...)):

    if password != valid_password:
        return templates.TemplateResponse('register.html', {"request":request})
    
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Todo: this is not the best practice, I set the DEFAULT values of two cols manully
    query_script = "INSERT INTO {} VALUES(?,?,?,1)".format(table_name) 
    cursor.execute(query_script, (None, username, password))

    connection.commit()
    connection.close()
    # return RedirectResponse(url='/user', status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse('login.html', {"request":request})