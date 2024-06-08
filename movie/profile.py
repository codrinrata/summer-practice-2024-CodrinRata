import datetime
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console
from rich.text import Text


console = Console()

import login as lg
import register as rg
import app as mn   
import post as ps
import time

import sqlite3
from rich.console import Console
from rich.table import Table
import os
import webbrowser

def get_user_feed(user_id):
    with sqlite3.connect("movie_app.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.id, p.full_title, p.released, p.imdb_rating, p.rotten_tomatoes_rating, 
                   p.user_rating, p.comments, p.watched_on, p.poster_link, p.imdbID,
                   p.timestamp, u.username, g.name AS group_name
            FROM posts p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN groups g ON p.group_id = g.id
            WHERE p.user_id = ? OR p.group_id IN (
                SELECT group_id FROM group_members WHERE user_id = ?
            )
            ORDER BY p.timestamp DESC
            """,
            (user_id, user_id),
        )
        return cursor.fetchall()

    
def handle_view_profile_feed(user_id):
    feed = get_user_feed(user_id)

    if not feed:
        print("Your feed is empty.")
        time.sleep(3)
        return

    table = Table(title="Your Feed", show_lines=True)
    table.add_column("ID", style= "dim")
    table.add_column("Full Title")
    table.add_column("Released")
    table.add_column("IMDb Rating")
    table.add_column("RT Rating")
    table.add_column("User Rating")
    table.add_column("Comments")
    table.add_column("Watched On")
    table.add_column("Poster Link")  # Uncomment to display poster links if available
    table.add_column("Posted By")
    table.add_column("Group")
    table.add_column("Timestamp")

    for row in feed:  # Iterate over rows directly
        # Format ratings and handle missing values
        imdb_rating_str = (
            f"{row[3]}/10" if row[3] is not None else Text("(Not available)", style="dim")
        )
        rt_rating_str = (
            row[10] if row[10] is not None else Text("(Not available)", style="dim")
        )

        imdb_base_url = "https://www.imdb.com/title/"

        imdb_id = row[4] if row[4] else None
        if imdb_id:
            full_title_link = "https://www.imdb.com/title/" + imdb_id
        else:
            full_title_link = row[1]

        # Add row to the table (adjust indices to match your query results)
        table.add_row(
            str(row[0]),
            f"[link={full_title_link}]{row[1]}[/link]",  # Full Title
            row[2] or "",  # Released date (or empty string if null)
            imdb_rating_str,
            rt_rating_str,
            str(row[5]),
            row[6] or "",
            row[7] or "",
            row[8],  # Uncomment to display poster link
            row[11], # Posted By
            row[12] or "",
            row[9],  # Timestamp
        )

    console.print(table)
    while True:
        action = input("Enter action (d to delete a post, q to quit): ").lower()
        if action == "d":
            post_id = int(input("Enter post ID to delete: "))
            ps.delete_post(post_id, user_id)
        elif action == "q":
            break
        

        else:
            print("Invalid action.")
