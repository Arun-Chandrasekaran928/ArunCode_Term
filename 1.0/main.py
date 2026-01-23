#Import Random & Sys & Json
import random
import sys
import json

#Seting FILESADMIN Not In Main() To Not Reset It Every Time.
FILESADMIN = []

#Adding Function main()
def main():
    #Making Main() Not Create It's Own FILESADMIN
    global FILESADMIN
    
    #Making A Forever Loop For The Main Menu So Program Doesn't End After Logout
    while True:
        #Try Loop Mainly Used To The Except Function
        try:
            #Printing Options:
	    #
	    #1) Login
	    #2) Create Acount
	    #3) Stay Logged Out (Guest)
	    #4) Exit
            print("\n1) Login")
            print("2) Create Account")
            print("3) Stay Logged Out (Guest)")
            print("4) Exit")

            #Seting Choise To An Input
            choice = input(">>> ")

            #Seting Hostname To ArunCode.ca
            hostname = "ArunCode.ca"

            #Seting Pwd To Home( ~/ )
            pwd = "~/"

            #Mainking Function Terminal With Sudo, Terminal_prompt, Username Files_list
            def terminal(sudo, terminal_prompt, username, files_list):
                #Try Loop Mainly Used To The Except Function
                try:
                    #Making A Forever Loop
                    while True:
                        #Setting Command To An Input
                        command = input(terminal_prompt)
                        
                        #Checking If Command = Whoami
                        if command == "whoami":
                            #Printing Username
                            print(username)
                        
                        #Checking If Command = Exit
                        elif command == "exit":
                            #Going To Main Menu
                            break

                        #Checking If Command = Ls 
                        elif command == "ls":
                            #Printing Files, If There Is No Files, Printing: (Directory Empty)
                            print("  ".join(files_list) if files_list else "(directory empty)")

                        #Checking If Command Startes With Touch
                        elif command.startswith("touch "):
                            #Spilting Command Into 2 Diffrent Groops: Touch, (Text) 
                            parts = command.split(" ", 1)
                            #Checking If Parts Has More Than 1 Groops
                            if len(parts) > 1:
                                #Seting The Second To: File_name
                                file_name = parts[1]
                                #Setting The Full Name To File_name + .Txt
                                full_name = file_name if file_name.endswith(".txt") else f"{file_name}.txt"
                                #Adding Full_name To Files_list
                                files_list.append(full_name)
                            else:
                                #Printing Touch: Missing File Operand
                                print("touch: missing file operand")

                        #Checking If Command Startes With Rm
                        elif command.startswith("rm "):
                            #Spilting Command Into 2 Diffrent Groops: Touch, (Text) 
                            parts = command.split(" ", 1)
                            #Checking If Parts Has More Than 1 Groops
                            if len(parts) > 1:
                                #Setting Files_to_remove To File_name
                                file_to_remove = parts[1]
                                #Checking If File_to_remove Does Not Cantain .Txt
                                if not file_to_remove.endswith(".txt"):
                                    #Adding .Txt To File_to_remove
                                    file_to_remove += ".txt"
                                #Checking If Files_to_remove Is In Files_list
                                if file_to_remove in files_list:
                                    #Removing Files_to_remove In Files_list
                                    files_list.remove(file_to_remove)
                                    #Printing Removed {File_to_remove}
                                    print(f"Removed {file_to_remove}")
                                else:
                                  #Printing Rm: Cannot Remove '{File_to_remove}': No Such File
                                    print(f"rm: cannot remove '{file_to_remove}': No such file")
                            else:
                                #Printing Rm: Missing Operand
                                print("rm: missing operand")

                        #Checking If Command = Sudo
                        elif command == "sudo":
                            #Printing Sudo Usage Text
                            print("usage: sudo -h | -K | -k | -V\nusage: sudo -v [-ABkNnS] [-g group] [-h host] [-p prompt] [-u user]\nusage: sudo -l [-ABkNnS] [-g group] [-h host] [-p prompt] [-U user] [-u user]\n            [command [arg ...]]\nusage: sudo [-ABbEHkNnPS] [-r role] [-t type] [-C num] [-D directory] [-g\n            group] [-h host] [-p prompt] [-R directory] [-T timeout] [-u user]\n[VAR=value] [-i | -s] [command [arg ...]]\nusage: sudo -e [-ABkNnS] [-r role] [-t type] [-C num] [-D directory] [-g group]\n[-h host] [-p prompt] [-R directory] [-T timeout] [-u user] file ...")

                #Excepting An Keyboard Interruption
                except KeyboardInterrupt:
                    #Printing Returning to Main Menu
                    print("\nReturning to Main Menu...")
                    return

            #Checking If Choice = 1 (Login Mode)
            if choice == "1":
                #Setting USER & PASS To An Input
                USER = input("user: ")
                PASS = input("pass: ")

                #Try To Load The JSON File
                try:
                    #Opening The Data File As Read Only
                    with open('username-password-data.json', 'r') as f:
                        #Converting JSON To Python List
                        accounts = json.load(f)
                    
                    #Checking If Credentials Match Any Entry In JSON
                    found_user = next((acc for acc in accounts if acc['username'] == USER and acc['password'] == PASS), None)

                    #If Match Found
                    if found_user:
                        #Checking If User Has Sudo Privileges In JSON
                        is_sudo = found_user.get("sudo") == "True"
                        #Setting Prompt Symbol Based On Sudo
                        symbol = "#" if is_sudo else "$"
                        #Runing Terminal Function With User Data
                        terminal(is_sudo, f"{found_user['username']}@{hostname}:{pwd} {symbol} ", found_user['username'], FILESADMIN)
                    else:
                        #Printing ERROR: Invalid Credentials 
                        print(" ERROR: Invalid Credentials ")
                
                #Excepting If The File Is Missing
                except FileNotFoundError:
                    print("ERROR: Database file 'username-password-data.json' not found.")

            #Checking If Choice = 2 (Create Account Mode)
            elif choice == "2":
                #Setting NEW_USER & NEW_PASS To An Input
                NEW_USER = input("Choose Username: ")
                NEW_PASS = input("Choose Password: ")

                #Try To Read And Update The JSON File
                try:
                    #Opening The File To Read Current Accounts
                    with open('username-password-data.json', 'r') as f:
                        accounts = json.load(f)
                    
                    #Checking If Username Already Exists
                    if any(acc['username'] == NEW_USER for acc in accounts):
                        print("ERROR: Username already taken!")
                    else:
                        #Creating New Account Dictionary With Sudo Set To False
                        new_account = {"username": NEW_USER, "password": NEW_PASS, "sudo": "False"}
                        #Adding New Account To The List
                        accounts.append(new_account)
                        #Opening The File To Write Updated List
                        with open('username-password-data.json', 'w') as f:
                            #Saving Data With 4-Space Indentation
                            json.dump(accounts, f, indent=4)
                        #Printing Success Message
                        print(f"Account for {NEW_USER} created successfully!")

                #Excepting If File Is Missing
                except FileNotFoundError:
                    print("ERROR: Database file not found.")

            #Checking If Choice = 3 (Guest Mode)
            elif choice == "3":
                #Setting FILESGUEST To []
                FILESGUEST = []
                #Setting Guest_name To geust + random number
                guest_name = "guest" + str(random.randint(1000, 9999))
                #Runing Terminal Function As Guest
                terminal(False, f"{guest_name}@{hostname}:{pwd} $ ", guest_name, FILESGUEST)

            #Checking If Choice = 4 (Exit Program)
            elif choice == "4":
                #Printing Exiting...
                print("Exiting...")
                #Exiting File
                sys.exit()

        #Excepting An Keyboard Interruption At Main Menu
        except KeyboardInterrupt:
            #Printing Exiting Program...
            print("\nExiting Program...")
            #Exiting File
            sys.exit()

#Checking If __Name__ = __Main__
if __name__ == "__main__":
    #Runing Function Main
    main()
