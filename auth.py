import sqlite3
import bcrypt

DB = "users.db"

# ---------- INIT DATABASE ----------
def init_db():

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB
    )
    """)

    conn.commit()
    conn.close()


# ---------- CREATE USER ----------
def create_user(username, password):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        c.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username, hashed)
        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:

        conn.close()
        return False


# ---------- LOGIN USER ----------
def login_user(username, password):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    result = c.fetchone()

    conn.close()

    if result:

        stored_hash = result[0]

        if bcrypt.checkpw(password.encode(), stored_hash):
            return True

    return False