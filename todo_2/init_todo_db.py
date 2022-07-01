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
create_table = """CREATE TABLE IF NOT EXISTS todo 
(id INTEGER PRIMARY KEY, 
item text, 
description text,
priority integer,
owner integer,
complete boolean default 0,
display boolean default 1,
foreign key(owner) references user(id) on delete cascade on update cascade
)
"""
cursor.execute(create_table)

sql = "INSERT INTO todo (item, description,priority,owner) VALUES (?, ?, ?, ?)"
val = ("Eat", "Eat 2 burger", "1", 1)
cursor.execute(sql, val)

sql = "INSERT INTO todo (item, description,priority,owner) VALUES (?, ?, ?, ?)"
val = ("Workout", "200 push ups", "2", 2)
cursor.execute(sql, val)

sql = "INSERT INTO todo (item, description,priority,owner) VALUES (?, ?, ?, ?)"
val = ("Sleep", "3 hour sleep", "3", 1)
cursor.execute(sql, val)

connection.commit()
connection.close()