import sqlite3

def create_user_table():
    conn = sqlite3.connect('Aquanav.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        )
        '''
    )

    conn.commit()
    conn.close()

create_user_table()
def register_user(username, email, password):
    conn = sqlite3.connect('Aquanav.db')
    cursor = conn.cursor()

    # password hashing

    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute('''
        INSERT INTO users (username, email, password)
        VALUES (?,?,?)
        ''', (username, email, password))

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_login(email, password):
    conn = sqlite3.connect('Aquanav.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM users WHERE email = ? AND password = ?''', (email, password))

    user = cursor.fetchone()
    conn.close()

    return user




