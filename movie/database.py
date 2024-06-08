import sqlite3

def create_database():
    conn = sqlite3.connect("movie_app.db")  # Creates or connects to the database file
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )

    # Create groups table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
        """
    )

    # Create group_members table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS group_members (
            group_id INTEGER,
            user_id INTEGER,
            is_admin INTEGER DEFAULT 0,
            FOREIGN KEY(group_id) REFERENCES groups(id),
            FOREIGN KEY(user_id) REFERENCES users(id),
            PRIMARY KEY(group_id, user_id) 
        )
        """
    )

    # Create posts table (updated)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            group_id INTEGER,
            full_title TEXT NOT NULL,
            released TEXT,
            imdb_rating REAL,
            rotten_tomatoes_rating REAL,
            user_rating INTEGER,
            comments TEXT,
            watched_on TEXT,
            poster_link TEXT,
            imdbID TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(group_id) REFERENCES groups(id)
        )
        """
    )

    conn.commit()  # Save changes
    conn.close()  # Close the connection

create_database()

# In other functions, connect to the database like this:
def some_function():
    with sqlite3.connect("movie_app.db") as conn:  
        cursor = conn.cursor()
        # Execute SQL commands here
