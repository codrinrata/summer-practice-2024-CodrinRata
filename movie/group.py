import sqlite3
import time


def get_group_id_from_user(user_id):
    with sqlite3.connect("movie_app.db") as conn:
        cursor = conn.cursor()

        # Fetch groups the user is a member of
        cursor.execute(
            """
            SELECT g.id, g.name 
            FROM groups g
            JOIN group_members gm ON g.id = gm.group_id
            WHERE gm.user_id = ?
            """,
            (user_id,),
        )
        groups = cursor.fetchall()

        if not groups:
            print("You are not a member of any groups.")
            return None

        # Display group choices to the user
        print("Choose a group:")
        for i, (group_id, group_name) in enumerate(groups):
            print(f"{i+1}. {group_name}")

        # Get user's group choice
        while True:
            try:
                choice = int(input("Enter the group number: ")) - 1
                if 0 <= choice < len(groups):
                    return groups[choice][0]  # Return the selected group's ID
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number.")

def create_group(name, description, user_id):
    with sqlite3.connect("movie_app.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO groups (name, description) VALUES (?, ?)",
                (name, description),
            )
            group_id = cursor.lastrowid  # Get the ID of the created group
            cursor.execute(
                "INSERT INTO group_members (group_id, user_id, is_admin) VALUES (?, ?, 1)",  # Creator is admin
                (group_id, user_id),
            )
            conn.commit()
            print("Group created successfully!")
            time.sleep(1)
        except sqlite3.IntegrityError:
            print("Group name already exists.")
            time.sleep(1)

def join_group(group_id, user_id):
    with sqlite3.connect("movie_app.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO group_members (group_id, user_id) VALUES (?, ?)",
                (group_id, user_id),
            )
            conn.commit()
            print("Joined group successfully!")
            time.sleep(1)
        except sqlite3.IntegrityError:
            print("You are already a member of this group.")
            time.sleep(1)

def get_available_groups(user_id):
    with sqlite3.connect("movie_app.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name 
            FROM groups 
            WHERE id NOT IN (
                SELECT group_id FROM group_members WHERE user_id = ?
            )
            """,
            (user_id,),
        )
        available_groups = cursor.fetchall()
        print(f"Available groups for user {user_id}: {available_groups}")  # Debug print
        return available_groups



def handle_create_group(user_id):
    name = input("Enter group name: ")
    description = input("Enter group description (optional): ")
    create_group(name, description, user_id)
    
def handle_join_group(user_id):
    available_groups = get_available_groups(user_id)
    print(f"Available Groups: {available_groups}")  # Debug print
    
    if not available_groups:
        print("No groups available to join.")
        time.sleep(1)
        return

    print("\nAvailable groups:")
    for i, (group_id, group_name) in enumerate(available_groups):
        print(f"{i+1}. {group_name}")
    
    while True:
        try:
            choice = int(input("Enter the group number to join: "))
            if 1 <= choice <= len(available_groups):
                selected_group_id = available_groups[choice - 1][0]
                join_group(selected_group_id, user_id)
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")


