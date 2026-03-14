import sqlite3
import datetime

DB="users.db"

def init_usage():

    conn=sqlite3.connect(DB)
    c=conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS usage(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        app TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_usage(username,app):

    conn=sqlite3.connect(DB)
    c=conn.cursor()

    c.execute(
        "INSERT INTO usage(username,app,time) VALUES(?,?,?)",
        (username,app,str(datetime.datetime.now()))
    )

    conn.commit()
    conn.close()