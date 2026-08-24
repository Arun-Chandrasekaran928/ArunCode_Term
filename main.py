import sys
import time
import shlex
import os
import json
import urllib.request
from utils import get_masked_input, run_real_nano

try:
    from werkzeug.security import check_password_hash
except ImportError:
    def check_password_hash(hash_str, plain_text):
        return hash_str == plain_text

BASE_URL = "http://192.168.1.110:5000"
HASH_STR = "scrypt:32768:8:1$unWMjmI0PN1WC29L$9e71c570a6064f50dc5ba5832007d645d3dbad7b13015f39fd0e30ff17f9d7bad4054e6b5b9c8f2c2231a3dd2719d409f2f82be3ed6f4f946bf1d6a14c702db6"

USERS_URL = f"{BASE_URL}/{HASH_STR}_users.json"
accounts = {}

try:
    with urllib.request.urlopen(USERS_URL, timeout=3) as response:
        server_data = json.loads(response.read().decode())
        accounts.update(server_data)
except Exception as e:
    print(f"[Warning] Remote database sync failed: {e}")

installed_apt = ["python3", "nano", "cat", "python"]
installed_pip = ["pip"]
BASE_DIR = os.path.abspath("./Admin")
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

def run_login_menu():
    while True:
        print("\n1) Login")
        print("2) Create Account")
        print("3) Guest")
        print("4) Exit")
        try:
            choice = input(">>> ").strip()
        except (KeyboardInterrupt, EOFError):
            return None

        if choice == "1":
            user = input("Username: ").strip()
            password = get_masked_input("Pass: ")
            pin = get_masked_input("PIN: ")
            
            if user in accounts:
                user_record = accounts[user]
                stored_pass = str(user_record.get("password", "")).strip()
                stored_pin = str(user_record.get("pin", "")).strip()
                
                if stored_pin == str(pin).strip():
                    if check_password_hash(stored_pass, str(password).strip()) or stored_pass == str(password).strip():
                        print("Login successful!\n")
                        return user
            print("Invalid credentials. Try again.")
        elif choice == "3":
            print("Logged in as Guest.\n")
            return "Guest"
        elif choice == "4":
            return None

current_user = run_login_menu()

if current_user is not None:
    while True:
        try:
            inp = input(f"{current_user}@://aruncode.com # ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExit"); break
        if not inp: continue
        
        try:
            parts = shlex.split(inp)
        except ValueError as e:
            print(f"Syntax error: {e}"); continue
            
        if not parts: continue
        cmd = parts[0]
        args = parts[1:]

        if cmd == "exit":
            print("Logging out...")
            break
            
        elif cmd == "clear":
            # Clears the terminal screen completely
            sys.stdout.write('\033[H\033[2J')
            sys.stdout.flush()
            
        elif cmd == "help":
            print("\nAvailable commands:")
            print("  ls            List files in the directory")
            print("  cat <file>    View the content of a file")
            print("  nano <file>   Open text editor interface")
            print("  rm <file>     Remove a file")
            print("  clear         Clear the terminal screen")
            print("  exit          Log out of the environment\n")

        elif cmd == "ls":
            files = os.listdir(BASE_DIR)
            print("  ".join(files) if files else "(directory empty)")

        elif cmd == "nano":
            if not args:
                print("nano: missing filename"); continue
            filename = args[0]
            run_real_nano(os.path.join(BASE_DIR, filename), filename)

        elif cmd == "cat":
            if not args:
                print("cat: missing filename"); continue
            filename = args[0]
            file_path = os.path.join(BASE_DIR, filename)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, "r") as f:
                    print(f.read())
            else:
                print(f"cat: {filename}: No such file")
            
        elif cmd == "rm":
            if not args:
                print("rm: missing operand"); continue
            filename = args[0]
            file_path = os.path.join(BASE_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Removed file: {filename}")
            else:
                print(f"rm: {filename}: No such file")

        elif cmd == "sudo":
            if len(args) >= 3 and args[0:2] == ["apt", "install"]:
                pkg = args[2]
                print("Reading package lists... Done\nBuilding dependency tree... Done")
                print(f"Unpacking {pkg}...\nSetting up {pkg}... Done")
                if pkg not in installed_apt: installed_apt.append(pkg)
            else:
                print("sudo: command not found or invalid apt syntax")
                
        elif cmd in ["pip", "pip3"]:
            if len(args) >= 2 and args[0] == "install":
                pkg = args[1]
                print(f"Collecting {pkg}\nSuccessfully installed {pkg}")
                if pkg not in installed_pip: installed_pip.append(pkg)
            else:
                print(f"Usage: {cmd} install <package>")

        elif cmd in installed_apt or cmd in installed_pip:
            if cmd == "git":
                print("usage: git [--version] [--help] <command> [<args>]")
            elif cmd in ["python", "python3"] and args:
                filename = args[0]
                file_path = os.path.join(BASE_DIR, filename)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, "r") as f:
                            exec(f.read(), {"__builtins__": __builtins__})
                    except Exception as e:
                        print(f"Python Runtime Error: {e}")
                else:
                    print(f"python: can't open file '{filename}': No such file")
            else:
                print(f"[{cmd}] mock: package running successfully.")
        else:
            print(f"{cmd}: command not found")
