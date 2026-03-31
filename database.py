import sqlite3
import hashlib

def connect():
    return sqlite3.connect("database.db", check_same_thread=False)


# CREATE TABLE
def create_tables():

    conn = connect()
    c = conn.cursor()

    # USERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    # HISTORY TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        username TEXT,
        cylinders INTEGER,
        displacement REAL,
        horsepower REAL,
        weight REAL,
        acceleration REAL,
        model_year INTEGER,
        mpg REAL,
        kmpl REAL,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    

# HASH PASSWORD
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


# LOGIN USER
def login_user(username,password):

    conn = connect()
    c = conn.cursor()

    hashed = make_hash(password)

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username,hashed))
    data = c.fetchone()

    conn.close()

    return data


# REGISTER USER
def add_user(username,password):

    conn = connect()
    c = conn.cursor()

    hashed = make_hash(password)

    c.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,hashed))

    conn.commit()
    conn.close()


# UPDATE USERNAME
def update_username(old_username,new_username):

    conn = connect()
    c = conn.cursor()

    c.execute("UPDATE users SET username=? WHERE username=?",(new_username,old_username))

    conn.commit()
    conn.close()


# UPDATE PASSWORD
def update_password(username,new_password):

    conn = connect()
    c = conn.cursor()

    hashed = make_hash(new_password)

    c.execute("UPDATE users SET password=? WHERE username=?",(hashed,username))

    conn.commit()
    conn.close()


# UPDATE APP PREFERENCES
def update_preferences(username,theme,notifications):

    conn = connect()
    c = conn.cursor()

    c.execute(
        "UPDATE users SET theme=?,notifications=? WHERE username=?",
        (theme,notifications,username)
    )

    conn.commit()
    conn.close()

def save_prediction(username,cyl,disp,hp,weight,acc,year,mpg,kmpl):

    conn = connect()
    c = conn.cursor()

    c.execute("""
    INSERT INTO history
    (username,cylinders,displacement,horsepower,weight,acceleration,model_year,mpg,kmpl)
    VALUES (?,?,?,?,?,?,?,?,?)
    """,(username,cyl,disp,hp,weight,acc,year,mpg,kmpl))

    conn.commit()
    conn.close()


def get_history(username):

    conn = connect()
    c = conn.cursor()

    c.execute("""SELECT username,cylinders,displacement,horsepower,
    weight,acceleration,model_year,mpg,kmpl,time
    FROM history WHERE username=?
    """,(username,))

    data = c.fetchall()

    conn.close()

    return data
