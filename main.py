#Import Random & Sys & Json
import random
import sys
import json

#Seting FILESADMIN Not In Main() To Not Reset It Every Time
FILESADMIN = []

#Adding Function main()
def main():
    #Making Main() Not Create It's Own FILESADMIN
    global FILESADMIN
    
    #Making A Forever Loop For The Main Menu
    while True:
        #Try Loop Mainly Used To The Except Function
        try:
            #Printing Options
            print("\n1) Login")
            print("2) Stay Logged Out (Guest)")
            print("3) Exit")

            #Seting Choise To An Input
            choice = input(">>> ")

            #Seting Hostname To ArunCode.ca
            hostname = "ArunCode.ca"

            #Seting Pwd To Home( ~/ )
            pwd = "~/"

            #Mainking Function Terminal
            def terminal(sudo, terminal_prompt, username, files_list):
                #Try Loop Mainly Used To The Except Function
                try:
                    #Making A Forever Loop
                    while True:
                        #Setting Command To An Input
                        command = input(terminal_prompt)
                        
                        #Checking If Command = Whoami
                        if command == "whoami":
                            print(username)
                        
                        #Checking If Command = Exit
                        elif command == "exit":
                            #Returning To Main Menu Loop
                            return

                        #Checking If Command = Ls 
                        elif command == "ls":
                            print("  ".join(files_list) if files_list else "(directory empty)")

                        #Checking If Command Startes With Touch
                        elif command.startswith("touch "):
                            parts = command.split(" ", 1)
                            if len(parts) > 1:
                                file_name = parts[1]
                                full_name = file_name if file_name.endswith(".txt") else f"{file_name}.txt"
                                files_list.append(full_name)
                            else:
                                print("touch: missing file operand")

                        #Checking If Command Startes With Rm
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

                        #Checking If Command = Sudo
                        elif command == "sudo":
                            print("usage: sudo -h | -K | -k | -V...")

                #Excepting An Keyboard Interruption
                except KeyboardInterrupt:
                    print("\nReturning to Main Menu...")
                    return

            #Checking If Choice = 1 (Login Mode)
            if choice == "1":

                #Setting USER_INPUT & PASS_INPUT To An Input
                USER_INPUT = input("user: ")
                PASS_INPUT = input("pass: ")

                #Try To Open The JSON Database File
                try:
                    #Opening username-password-data.json As Read Only
                    with open('username-password-data.json', 'r') as f:
                        #Loading JSON Content Into A List Called Accounts
                        accounts = json.load(f)
                
                #Excepting If File Is Missing
                except FileNotFoundError:
                    #Printing Error If File Not Found
                    print("ERROR: Database file not found.")
                    #Continuing To Next Loop Iteration
                    continue

                #Setting Logged_In User Data To None
                found_user = None

                #Looping Through Every Account In The JSON List
                for acc in accounts:
                    #Checking If Input Matches Username AND Password From JSON
                    if acc['username'] == USER_INPUT and acc['password'] == PASS_INPUT:
                        #Setting found_user To The Dictionary Of That Account
                        found_user = acc
                        #Stopping The Loop Because We Found A Match
                        break

                #Checking If A Match Was Found
                if found_user:
                    #Checking If Sudo Is Set To "True" String In JSON
                    is_sudo = found_user.get("sudo") == "True"
                    #Setting Symbol To # If Sudo, Else $
                    symbol = "#" if is_sudo else "$"
                    
                    #Running Terminal With User Data From JSON
                    terminal(is_sudo, f"{found_user['username']}@{hostname}:{pwd} {symbol} ", found_user['username'], FILESADMIN)
                
                #Checking If No Match Was Found
                else:
                    #Printing Invalid Credentials Error
                    print(" ERROR: Invalid Credentials ")

            #Checking If Choice = 2 (Guest Mode)
            elif choice == "2":
                FILESGUEST = []
                guest_name = "guest" + str(random.randint(1000, 9999))
                terminal(False, f"{guest_name}@{hostname}:{pwd} $ ", guest_name, FILESGUEST)

            #Checking If Choice = 3 (Exit)
            elif choice == "3":
                print("Exiting...")
                sys.exit()

        #Excepting Keyboard Interruption On Main Menu
        except KeyboardInterrupt:
            print("\nExiting Program...")
            sys.exit()

#Checking If __Name__ = __Main__
if __name__ == "__main__":
    #Starting Main Function
    main()
