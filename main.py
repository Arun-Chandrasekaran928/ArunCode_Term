import random
import sys


FILESADMIN = []

def main():
    global FILESADMIN
    
    try:
        print("\n1) Login")
        print("2) Stay Logged Out (Guest)")
        print("3) Exit")

        choice = input(">>> ")
        hostname = "ArunCode.ca"
        pwd = "~/"

        def terminal(sudo, terminal_prompt, username, files_list):
            try:
                while True:
                    command = input(terminal_prompt)
                    
                    if command == "whoami":
                        print(username)
                    
                    elif command == "exit":
                        break

                    elif command == "ls":
                        print("  ".join(files_list) if files_list else "(directory empty)")

                    elif command.startswith("touch "):
                        parts = command.split(" ", 1)
                        if len(parts) > 1:
                            file_name = parts[1]

                            full_name = file_name if file_name.endswith(".txt") else f"{file_name}.txt"
                            files_list.append(full_name)
                        else:
                            print("touch: missing file operand")

                    elif command.startswith("rm "):
                        parts = command.split(" ", 1)
                        if len(parts) > 1:
                            file_to_remove = parts[1]

                            if not file_to_remove.endswith(".txt"):
                                file_to_remove += ".txt"
                            
                            if file_to_remove in files_list:
                                files_list.remove(file_to_remove)
                                print(f"Removed {file_to_remove}")
                            else:
                                print(f"rm: cannot remove '{file_to_remove}': No such file")
                        else:
                            print("rm: missing operand")

                    elif command == "sudo":
                        print("usage: sudo -h | -K | -k | -V\nusage: sudo -v [-ABkNnS] [-g group] [-h host] [-p prompt] [-u user]\nusage: sudo -l [-ABkNnS] [-g group] [-h host] [-p prompt] [-U user] [-u user]\n            [command [arg ...]]\nusage: sudo [-ABbEHkNnPS] [-r role] [-t type] [-C num] [-D directory] [-g\n            group] [-h host] [-p prompt] [-R directory] [-T timeout] [-u user]\n[VAR=value] [-i | -s] [command [arg ...]]\nusage: sudo -e [-ABkNnS] [-r role] [-t type] [-C num] [-D directory] [-g group]\n[-h host] [-p prompt] [-R directory] [-T timeout] [-u user] file ...")

                            
            except KeyboardInterrupt:
                print("\nReturning to Main Menu...")
                return

        if choice == "1":
            USER = input("user: ")
            PASS = input("pass: ")

            if USER == "Arun C." and PASS == "927927":
                admin_name = "Admin"
                terminal(True, f"{admin_name}@{hostname}:{pwd} # ", admin_name, FILESADMIN)
            else:
                print(" ERROR: Invalid Credentials ")

        elif choice == "2":
            FILESGUEST = []
            guest_name = "guest" + str(random.randint(1000, 9999))
            terminal(False, f"{guest_name}@{hostname}:{pwd} $ ", guest_name, FILESGUEST)

        elif choice == "3":
            print("Exiting...")
            sys.exit()

        if choice != "3":
            main()

    except KeyboardInterrupt:
        print("\nExiting Program...")
        sys.exit()

if __name__ == "__main__":
    main()
