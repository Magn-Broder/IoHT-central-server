from passlib.hash import sha256_crypt
import sqlite3

DATABASE = 'database.db'

def get_db_connection():
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        return connection

def register_user_to_db(first_name, last_name, username, password, confirm_password):
    if password != confirm_password:
        print("Passwords er ikke ens")
        return False
    
    hashed_password = sha256_crypt.encrypt(password)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO login (firstname, lastname, username, password) VALUES (?, ?, ?, ?)', (first_name, last_name, username, hashed_password))
    conn.commit()
    return True

while True:
    print("Type your choice followed by Enter")
    print("1) Registre a new user. 2) Exit the program.")

    user_input = input("Type your choice followed by Enter: ")

    if user_input == "1":
        firstname = input("Hvad er fornavnet? ")
        lastname = input("Hvad er efternavnet? ")
        username = input("Angiv et username: ")
        password = input("Angiv et password: ")
        confirm_password = input("Bekræft password: ")
        register_user_to_db(firstname, lastname, username, password, confirm_password)

    if user_input == "2":
        break
    
    else:
        print("-Invalid input-")
