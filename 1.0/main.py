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
# sudo     → True / False
# username → current username
# fs       → user's filesystem
def terminal(sudo, username, fs):

    # Root directory
    root = fs

    # Current working directory
    cwd = root

    # Stack to track path
    path_stack = []

    hostname = "ArunCode.ca"

    try:
        # Forever loop so terminal stays open
        while True:

            # Building path string
            path = "/" + "/".join(path_stack) if path_stack else "~"
            command = input(f"{username}@{hostname}:{path} $ ")

            # ---------- whoami ----------
            if command == "whoami":
                print(username)

            # ---------- exit ----------
            elif command == "exit":
                break

            # ---------- ls ----------
            elif command == "ls":
                items = list(cwd["folders"].keys()) + cwd["files"]
                print("  ".join(items) if items else "(directory empty)")

            # ---------- makir ----------
            # Custom command to make a directory
            elif command.startswith("makir "):
                name = command.split(" ", 1)[1]

                # Check if folder already exists
                if name in cwd["folders"]:
                    print("makir: folder exists")
                else:
                    cwd["folders"][name] = {
                        "files": [],
                        "folders": {}
                    }

            # ---------- touch ----------
            elif command.startswith("touch "):
                name = command.split(" ", 1)[1]
                if not name.endswith(".txt"):
                    name += ".txt"

                if name in cwd["files"]:
                    print("touch: file exists")
                else:
                    cwd["files"].append(name)

            # ---------- rm ----------
            elif command.startswith("rm "):
                name = command.split(" ", 1)[1]
                if not name.endswith(".txt"):
                    name += ".txt"

                if name in cwd["files"]:
                    cwd["files"].remove(name)
                    print(f"Removed {name}")
                else:
                    print(f"rm: cannot remove '{name}'")

            # ---------- cd ----------
            elif command.startswith("cd"):
                parts = command.split(" ", 1)

                # cd or cd ~ → go home
                if len(parts) == 1 or parts[1] == "~":
                    cwd = root
                    path_stack = []

                # cd .. → go back
                elif parts[1] == "..":
                    if path_stack:
                        path_stack.pop()
                        cwd = root
                        for p in path_stack:
                            cwd = cwd["folders"][p]

                # cd folder_name
                else:
                    folder = parts[1]
                    if folder in cwd["folders"]:
                        cwd = cwd["folders"][folder]
                        path_stack.append(folder)
                    else:
                        print(f"cd: no such directory: {folder}")

            # ---------- sudo ----------
            elif command == "sudo":
                print("usage: sudo [command]")

            # ---------- unknown ----------
            else:
                print(f"{command}: command not found")

    except KeyboardInterrupt:
        print("\nReturning to Main Menu...")
        return


# ---------- MAIN FUNCTION ----------
def main():

    while True:
        try:
            print("\n1) Login")
            print("2) Create Account")
            print("3) Stay Logged Out (Guest)")
            print("4) Exit")

            choice = input(">>> ")

            # ---------- LOGIN ----------
            if choice == "1":
                USER = input("user: ")
                PASS = input("pass: ")

                with open(DATA_FILE, "r") as f:
                    accounts = json.load(f)

                user = next(
                    (a for a in accounts
                     if a["username"] == USER and a["password"] == PASS),
                    None
                )

                if user:
                    terminal(user["sudo"] == "True", USER, user["fs"])

                    # Save filesystem after logout
                    with open(DATA_FILE, "w") as f:
                        json.dump(accounts, f, indent=4)
                else:
                    print("ERROR: Invalid credentials")

            # ---------- CREATE ACCOUNT ----------
            elif choice == "2":
                NEW_USER = input("Choose Username: ")
                NEW_PASS = input("Choose Password: ")

                with open(DATA_FILE, "r") as f:
                    accounts = json.load(f)

                if any(a["username"] == NEW_USER for a in accounts):
                    print("ERROR: Username already taken")
                else:
                    accounts.append({
                        "username": NEW_USER,
                        "password": NEW_PASS,
                        "sudo": "False",
                        "fs": {
                            "files": [],
                            "folders": {}
                        }
                    })

                    with open(DATA_FILE, "w") as f:
                        json.dump(accounts, f, indent=4)

                    print(f"Account for {NEW_USER} created successfully")

            # ---------- GUEST ----------
            elif choice == "3":
                guest_name = "guest" + str(random.randint(1000, 9999))
                guest_fs = {
                    "files": [],
                    "folders": {}
                }
                terminal(False, guest_name, guest_fs)

            # ---------- EXIT ----------
            elif choice == "4":
                print("Exiting...")
                sys.exit()

            else:
                print("Invalid option")

        except KeyboardInterrupt:
            print("\nExiting Program...")
            sys.exit()


# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    main()
