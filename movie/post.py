import datetime
import webbrowser
from rich.console import Console
import sqlite3
import time
from numpy import double
import requests
import group as gp

console = Console()

def fetch_movie_details(title, year):  
    api_key = "30c2b765"  
    base_url = "http://www.omdbapi.com/"
    params = {
        "apikey": api_key,
        "t": title,
        "y": year,
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data["Response"] == "True":
            return (
                data.get("Title"),  # Full title
                data.get("Released"),  # Exact release date
                data.get("imdbRating"),
                data.get("imdbID"),
                data.get("Ratings", [{}])[1].get("Value"),
                data.get("Poster"),
                
            )
        else:
            print("Movie not found in OMDb.")
            return None, None, None, None, None, None  # Return None values if not found
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie details: {e}")
        time.sleep(2)
        return None, None, None, None, None

def create_post(
    user_id,
    full_title, # Use full_title directly
    released,    # Use released directly
    user_rating,
    comments,
    watched_on,
    imdbID = None,
    group_id=None,
    imdb_rating=None,
    rotten_tomatoes_rating=None,
    poster_link=None,
    
):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Fetch movie details (if not provided)
    if not imdb_rating or not rotten_tomatoes_rating or not poster_link or not imdbID:
        full_title, released, imdb_rating, rotten_tomatoes_rating, poster_link, imdbID = fetch_movie_details(
            full_title, released
        )
    
    # Insert into database (using full_title and released directly)
    with sqlite3.connect("movie_app.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO posts (
                user_id, group_id, full_title, released, imdb_rating, 
                rotten_tomatoes_rating, user_rating, comments, watched_on, poster_link, timestamp, imdbID
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                group_id,
                full_title,  
                released,
                imdb_rating,
                rotten_tomatoes_rating,
                user_rating,
                comments,
                watched_on,
                imdbID,
                poster_link,
                timestamp,
            ),
        )
        conn.commit()


def handle_create_post(user_id):
    title = input("Enter movie title: ")
    year = int(input("Enter movie year: "))
    user_rating = double(input("Enter your rating (1-10): "))
    comments = input("Enter your comments: ")
    watched_on = input("Where did you watch it? ")

    # Optionally, ask if the post is for a group
    while True:
        group_choice = input("Is this post for a group? (y/n): ").lower()
        if group_choice in ("y", "n"):
            break
        print("Invalid choice. Please enter 'y' or 'n'.")

    if group_choice == "y":
        group_id = gp.get_group_id_from_user(user_id)  # Pass user_id as argument
    else:
        group_id = None
    create_post(
        user_id,
        title,
        year,
        user_rating,
        comments,
        watched_on,
        group_id,
    )  # Pass all the information to create_post
    console.clear()
    print("Post created successfully!")
    time.sleep(1)

def delete_post(post_id, user_id):
    with sqlite3.connect("movie_app.db") as conn:
        cursor = conn.cursor()

        # Check if the user owns the post
        cursor.execute("SELECT user_id, group_id FROM posts WHERE id = ?", (post_id,))
        row = cursor.fetchone()

        if not row:
            print("Post not found.")
            return

        post_owner_id, group_id = row

        if post_owner_id != user_id:
            if group_id is not None:
                # Check if the user is an admin of the group
                cursor.execute(
                    "SELECT * FROM group_members WHERE group_id = ? AND user_id = ? AND is_admin = 1",
                    (group_id, user_id),
                )
                is_admin = cursor.fetchone() is not None
                if not is_admin:
                    print("You don't have permission to delete this post.")
                    return
            else:
                print("You don't have permission to delete this post.")
                return

        # Delete the post
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        print("Post deleted successfully.")
