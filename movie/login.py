from rich import print
from rich.prompt import Prompt
from rich.table import Table
import bcrypt
import csv
import sqlite3
import app as mn


def login(username, password):
    with sqlite3.connect("movie_app.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE username = ?", (username,)
        )  # Fetch the user_id and hash
        row = cursor.fetchone()

        if row:
            user_id, stored_hash = row  # Unpack id and hash
            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                return user_id  # Return the user_id on successful login
    return None  # Return None for invalid credentials

# ...

def handle_login():
    username = input("Username: ")
    password = Prompt.ask("Enter your password", password=True)
    user_id = login(username, password) 
    if user_id:
        print("Login successful!")
        while True:
            mn.main_menu(user_id)
    else:
        print("Invalid username or password.")

