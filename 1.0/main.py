# =========================
# main.py
# =========================

# ---------- IMPORTS ----------
# Import random for guest usernames
# Import sys for exiting program
# Import json for reading/writing accounts
# Import os for file paths
import random
import sys
import json
import os


# ---------- FILE PATH SETUP ----------
# Getting the path of this file so data.json is always found
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Creating the full path to data.json
DATA_FILE = os.path.join(BASE_DIR, "data.json")


# ---------- TERMINAL FUNCTION ----------
# sudo        → True / False
# prompt      → terminal prompt
# username    → current user
# files_list  → user's files
# folder_list → user's folders
def terminal(sudo, prompt, username, files_list, folder_list):

    # Try block to catch Ctrl+C
    try:
        # Forever loop so terminal stays open
        while True:
            # Getting command input
            command = input(prompt)

            # ---------- whoami ----------
            if command == "whoami":
                print(username)

            # ---------- exit ----------
            elif command == "exit":
                break

            # ---------- ls ----------
            elif command == "ls":
                items = folder_list + files_list
                print("  ".join(items) if items else "(directory empty)")

            # ---------- touch ----------
            elif command.startswith("touch "):
                parts = command.split(" ", 1)
                if len(parts) > 1:
                    file_name = parts[1]
                    if not file_name.endswith(".txt"):
                        file_name += ".txt"
                    files_list.append(file_name)
                else:
                    print("touch: missing file operand")

            # ---------- rm ----------
            elif command.startswith("rm "):
                parts = command.split(" ", 1)
                if len(parts) > 1:
                    file_name = parts[1]
                    if not file_name.endswith(".txt"):
                        file_name += ".txt"
                    if file_name in files_list:
                        files_list.remove(file_name)
                        print(f"Removed {file_name}")
                    else:
                        print(f"rm: cannot remove '{file_name}': No such file")
                else:
                    print("rm: missing operand")

            # ---------- mkdir ----------
            elif command.startswith("mkdir "):
                parts = command.split(" ", 1)
                if len(parts) > 1:
                    folder_list.append(parts[1])
                else:
                    print("mkdir: missing operand")

            # ---------- sudo ----------
            elif command == "sudo":
                print("usage: sudo [command]")

            # ---------- unknown ----------
            else:
                print(f"{command}: command not found")

    # Catch Ctrl+C inside terminal
    except KeyboardInterrupt:
        print("\nReturning to Main Menu...")
        return


# ---------- MAIN FUNCTION ----------
def main():

    hostname = "ArunCode.ca"
    pwd = "~/"

    # Forever loop for main menu
    while True:
        try:
            # ---------- MENU ----------
            print("\n1) Login")
            print("2) Create Account")
            print("3) Stay Logged Out (Guest)")
            print("4) Exit")

            choice = input(">>> ")

            # ---------- LOGIN ----------
            if choice == "1":
                USER = input("user: ")
                PASS = input("pass: ")

                try:
                    # Load database
                    with open(DATA_FILE, "r") as f:
                        accounts = json.load(f)

                    # Find matching account
                    user = next(
                        (a for a in accounts
                         if a["username"] == USER and a["password"] == PASS),
                        None
                    )

                    # If user found
                    if user:
                        is_sudo = user["sudo"] == "True"
                        symbol = "#" if is_sudo else "$"

                        # Start terminal with ACCOUNT-SPECIFIC storage
                        terminal(
                            is_sudo,
                            f"{USER}@{hostname}:{pwd} {symbol} ",
                            USER,
                            user["files"],
                            user["folders"]
                        )

                        # Save changes after logout
                        with open(DATA_FILE, "w") as f:
                            json.dump(accounts, f, indent=4)

                    else:
                        print("ERROR: Invalid credentials")

                except FileNotFoundError:
                    print("ERROR: Database file not found")

            # ---------- CREATE ACCOUNT ----------
            elif choice == "2":
                NEW_USER = input("Choose Username: ")
                NEW_PASS = input("Choose Password: ")

                try:
                    with open(DATA_FILE, "r") as f:
                        accounts = json.load(f)

                    # Check username
                    if any(a["username"] == NEW_USER for a in accounts):
                        print("ERROR: Username already taken")
                    else:
                        # Create new account WITH files and folders
                        accounts.append({
                            "username": NEW_USER,
                            "password": NEW_PASS,
                            "sudo": "False",
                            "files": [],
                            "folders": []
                        })

                        with open(DATA_FILE, "w") as f:
                            json.dump(accounts, f, indent=4)

                        print(f"Account for {NEW_USER} created successfully")

                except FileNotFoundError:
                    print("ERROR: Database file not found")

            # ---------- GUEST ----------
            elif choice == "3":
                guest_files = []
                guest_folders = []
                guest_name = "guest" + str(random.randint(1000, 9999))

                terminal(
                    False,
                    f"{guest_name}@{hostname}:{pwd} $ ",
                    guest_name,
                    guest_files,
                    guest_folders
                )

            # ---------- EXIT ----------
            elif choice == "4":
                print("Exiting...")
                sys.exit()

            else:
                print("Invalid option")

        # Ctrl+C in main menu
        except KeyboardInterrupt:
            print("\nExiting Program...")
            sys.exit()


# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    main()
