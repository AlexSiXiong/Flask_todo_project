import argparse
import sqlite3

def examine(db_name):
    connection = sqlite3.connect('todo.db')

    cursor = connection.cursor()

    sql_script = "select password, id from {} where name='{}'".format(db_name, 'bbd')
    res = cursor.execute(sql_script)
    save_password = res.fetchone()
    print(save_password)
    connection.close()
    
    connection.close()

def make_args():
    parser = argparse.ArgumentParser(
        description="Assign a database name that is to be examined."
    )

    parser.add_argument(
        "--table",
        type=str,
        help="The table name",
        default="user"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = make_args()
    examine(args.table)