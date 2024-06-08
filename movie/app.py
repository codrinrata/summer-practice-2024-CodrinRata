from rich import print
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console
import sys
import login as lg
import register as rg
import profile as pf
import post as ps
import group as gr

console = Console(width=300, height=30, record=True)  # Adjust width and height as needed

def create_group():
    print("[bold blue]Create Group[/bold blue]")
    group_name = Prompt.ask("Enter group name")
    # Create a new group
    print(f"Group {group_name} created successfully")


def quit():
    print("Exiting program...")
    sys.exit(0)  # Exit with success code 0


def main_menu(user_id, menu_stack=[]):
    console.clear()
    print("[bold blue]Main Menu[/bold blue]")
    print("1. Create/Join Groups")
    print("2. View Group Recommendations")
    print("3. Profile")
    print("4. Create post")
    print("0. Back")  
    print("q. Quit")
    
    # ... (handle input and call other functions, adding them to menu_stack if needed)
    
    choice = Prompt.ask("Enter your choice", choices=["0", "1", "2", "3", "4", "q"])  # Include "0" and "q"
    
    if choice == "0" and menu_stack:
        previous_menu = menu_stack.pop()
        previous_menu(user_id, menu_stack)  # Call the previous menu function
    if choice == "1":
        console.clear()
        group_menu(user_id)
    if choice == "3":
        console.clear()
        pf.handle_view_profile_feed(user_id)
    if choice == "4":
        console.clear()
        ps.handle_create_post(user_id)
    if choice == "0":
        console.clear()
        start_menu()
    elif choice == "q":
        console.clear()
        quit()  # Exit the main_menu function
    # ... (handle other choices)


def group_menu(user_id):
    console.clear()
    print("[bold blue]Group Menu[/bold blue]")
    print("1. Create Group")  
    print("2. Join Group")
    print("0. Back")
    choice = Prompt.ask("Enter your choice", choices=["1", "2", "0"])
    if choice == "1":
        console.clear()
        gr.handle_create_group(user_id)
    elif choice == "2":
        console.clear()
        gr.handle_join_group(user_id)

def start_menu():
    console.clear()
    print("[bold blue]Login Menu[/bold blue]")
    print("1. Login")
    print("2. Register")
    print("q. Exit")
    choice = Prompt.ask("Enter your choice", choices=["1", "2", "q"])
    
    if choice == "1":
        console.clear()
        lg.handle_login()
    if choice == "2":
        console.clear()
        rg.register()
    if choice == "q":
        console.clear()
        quit()

if __name__ == "__main__":
        start_menu()