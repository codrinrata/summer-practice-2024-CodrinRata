from rich import print
from rich.prompt import Prompt
from rich.table import Table

import bcrypt
import sqlite3
import app as mn
import login as lg

def register():
    while True:
        username = Prompt.ask("Enter your username")

        with sqlite3.connect("movie_app.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                print("Username already exists!")
                continue  # Ask for username again

            password = Prompt.ask("Enter your password", password=True)  # Hide password input
            password_confirm = Prompt.ask("Enter your password again", password=True)
            if password == password_confirm:
                add_credentials(username, password)
                print("Registration successful!")
                user_id = lg.login(username, password) 
                while True:
                    mn.main_menu(user_id)
                break  # Exit the loop
            else:
                print("Passwords do not match. Retrying!")


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()


def add_credentials(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with sqlite3.connect("movie_app.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed_password.decode()),
        )  # Decode hash back to string
        conn.commit()
