# =========================
# main.py
# =========================

# ---------- IMPORTS ----------
import random
import sys
import json
import os
import subprocess

# ---------- FILE PATH ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

# ---------- TERMINAL ----------
def terminal(user):

    hostname = "ArunCode.com"

    # Current directory reference (starts at root)
    cwd = user["fs"]
    path_stack = ["~"]

    def prompt():
        path = "/".join(path_stack)
        symbol = "#" if user["sudo"] == "True" else "$"
        return f"{user['username']}@{hostname}/{user['usertype']}:{path} {symbol} "

    try:
        while True:
            command = input(prompt()).strip()

            # ---------- whoami ----------
            if command == "whoami":
                print(user["username"])

            # ---------- exit ----------
            elif command == "exit":
                break

            # ---------- ls ----------
            elif command == "ls":
                items = list(cwd["folders"].keys()) + cwd["files"]
                print("  ".join(items) if items else "(directory empty)")

            # ---------- cd ----------
            elif command.startswith("cd"):
                parts = command.split()
                if len(parts) == 1 or parts[1] == "~":
                    cwd = user["fs"]
                    path_stack[:] = ["~"]
                elif parts[1] == "..":
                    if len(path_stack) > 1:
                        path_stack.pop()
                        cwd = user["fs"]
                        for p in path_stack[1:]:
                            cwd = cwd["folders"][p]
                elif parts[1] in cwd["folders"]:
                    cwd = cwd["folders"][parts[1]]
                    path_stack.append(parts[1])
                else:
                    print("cd: no such directory")

            # ---------- touch ----------
            elif command.startswith("touch "):
                name = command.split(" ", 1)[1]
                if not name.endswith(".txt"):
                    name += ".txt"
                if name not in cwd["files"]:
                    cwd["files"].append(name)

            # ---------- rm ----------
            elif command.startswith("rm "):
                name = command.split(" ", 1)[1]
                if not name.endswith(".txt"):
                    name += ".txt"
                if name in cwd["files"]:
                    cwd["files"].remove(name)
                else:
                    print("rm: no such file")

            # ---------- makir ----------
            elif command.startswith("makir "):
                name = command.split(" ", 1)[1]
                if name not in cwd["folders"]:
                    cwd["folders"][name] = {"files": [], "folders": {}}

            # ---------- nano ----------
            elif command.startswith("nano "):
                name = command.split(" ", 1)[1]
                if not name.endswith(".txt"):
                    name += ".txt"

                if name not in cwd["files"]:
                    cwd["files"].append(name)

                temp_file = f"/tmp/{user['username']}_{name}"
                open(temp_file, "a").close()
                subprocess.run(["nano", temp_file])

            # ---------- ping ----------
            elif command.startswith("ping "):
                target = command.split(" ", 1)[1]
                try:
                    subprocess.run(["ping", "-c", "4", target])
                except FileNotFoundError:
                    print("ping: command not found")

            # ---------- sudo ----------
            elif command == "sudo":
                print("usage: sudo [command]")

            # ---------- unknown ----------
            else:
                print(f"{command}: command not found")

    except KeyboardInterrupt:
        print("\nReturning to main menu...")


# ---------- MAIN ----------
def main():

    while True:
        try:
            print("\n1) Login")
            print("2) Create Account")
            print("3) Guest")
            print("4) Exit")

            choice = input(">>> ")

            # ---------- LOGIN ----------
            if choice == "1":
                u = input("user: ")
                p = input("pass: ")

                with open(DATA_FILE, "r") as f:
                    accounts = json.load(f)

                user = next(
                    (a for a in accounts if a["username"] == u and a["password"] == p),
                    None
                )

                if user:
                    terminal(user)
                    with open(DATA_FILE, "w") as f:
                        json.dump(accounts, f, indent=4)
                else:
                    print("ERROR: Invalid credentials")

            # ---------- CREATE ----------
            elif choice == "2":
                u = input("Choose Username: ")
                p = input("Choose Password: ")
                t = input("User Type: ")

                with open(DATA_FILE, "r") as f:
                    accounts = json.load(f)

                if any(a["username"] == u for a in accounts):
                    print("ERROR: Username exists")
                else:
                    accounts.append({
                        "username": u,
                        "password": p,
                        "sudo": "False",
                        "usertype": t,
                        "fs": {"files": [], "folders": {}}
                    })
                    with open(DATA_FILE, "w") as f:
                        json.dump(accounts, f, indent=4)
                    print("Account created")

            # ---------- GUEST ----------
            elif choice == "3":
                guest = {
                    "username": "guest" + str(random.randint(1000, 9999)),
                    "sudo": "False",
                    "usertype": "Guest",
                    "fs": {"files": [], "folders": {}}
                }
                terminal(guest)

            # ---------- EXIT ----------
            elif choice == "4":
                sys.exit()

        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit()


# ---------- ENTRY ----------
if __name__ == "__main__":
    main()
