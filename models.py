from passlib.hash import sha256_crypt
import sqlite3

DATABASE = 'database.db' # her sættes sti/til/database.db

def get_db_connection():
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        return connection
    
def initialize_database():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS login (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname, lastname, username TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS heartdata (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, bpm INT)')
    conn.execute('CREATE TABLE IF NOT EXISTS falls (id INTEGER PRIMARY KEY AUTOINCREMENT, patient, status, timestamp DATETIME, coordinates VARCHAR)')
    conn.commit()

def log_heart_data(bpm):
    conn = get_db_connection()
    conn.execute("INSERT INTO heartdata (timestamp, bpm) VALUES (DATETIME('now'), ?)", (bpm,))
    conn.commit()

def log_fall_data(coordinates):
    patient = "N/A"
    status = "faldet"
    conn = get_db_connection()
    conn.execute("INSERT INTO falls (patient, status, timestamp, coordinates) VALUES (?, ?, DATETIME('now'), ?)", (patient, status, coordinates))
    conn.commit()

def register_user_to_db(first_name, last_name, username, password, confirm_password):
    if password != confirm_password:
        return False  # Passwords do not match
    
    hashed_password = sha256_crypt.encrypt(password)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO login (firstname, lastname, username, password) VALUES (?, ?, ?, ?)', (first_name, last_name, username, hashed_password))
    conn.commit()
    return True

def check_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT password FROM login WHERE username = ?', (username,))
    row = cur.fetchone()

    if row:
        hashed_password = row[0]
        if sha256_crypt.verify(password, hashed_password):
            return True
    return False

def query_heart_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT timestamp, bpm FROM heartdata")
    data = cur.fetchall()
    return data

def query_fall_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM falls ORDER BY timestamp ASC')
    data = cur.fetchall()
    return data

initialize_database()