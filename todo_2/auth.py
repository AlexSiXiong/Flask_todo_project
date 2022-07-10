from datetime import datetime, timedelta
from http.client import HTTPException
from pickletools import StackObject
from telnetlib import STATUS
from tempfile import TemporaryFile
from fastapi import FastAPI, Depends
import sqlite3

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

db_name = 'todo.db'
table_name = 'user'

@app.get("/")
async def enter():
    return {'msg': 'hello world'}, 200

@app.post("/token")
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


async def decode_cur_user(cur_token=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(cur_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name = payload.get('sub')
        user_id = payload.get('id')
        if user_name is None or user_id is None:
            raise HTTPException(STATUS=404, detail='User not found')
        return {
            "user_name": user_name,
            "user_id": user_id
        }
    except JWTError:
        raise HTTPException(STATUS=404, detail='JWT error')

def create_access_token(user_name, user_id):
    expire_time = datetime.utcnow() + timedelta(15) # expire 15 min
    
    encode = {
        "sub": user_name, 
        "id": user_id,
        "exp": expire_time
    }

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
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