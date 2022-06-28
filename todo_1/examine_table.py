import argparse
import sqlite3

def examine(db_name):
    connection = sqlite3.connect('todo.db')

    cursor = connection.cursor()

    sql_script = "select * from {}".format(db_name)
    cursor.execute(sql_script)

    for i in cursor:
        print(i)
    
    connection.close()

def make_args():
    parser = argparse.ArgumentParser(
        description="Assign a database name that is to be examined."
    )

    parser.add_argument(
        "--table",
        type=str,
        help="The table name",
        default="todo"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = make_args()
    examine(args.table)