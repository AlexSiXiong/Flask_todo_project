import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1.db session init
# reference: https://fastapi.tiangolo.com/tutorial/sql-databases/
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 2.insert infomation into db
connection = sqlite3.connect('todo.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = """CREATE TABLE IF NOT EXISTS user 
(id INTEGER PRIMARY KEY, 
name varchar, 
password varchar,
activate boolean default 1
)
"""
cursor.execute(create_table)

sql = "INSERT INTO user (name, password) VALUES (?, ?)"
val = [
    ('user1', '123'),
    ('user2', '111')
]
cursor.executemany(sql, val)


connection.commit()
connection.close()