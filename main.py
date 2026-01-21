#Import Random & Sys
import random
import sys

#Seting FILESADMIN Not In Main() To Not Reset It Every Time
FILESADMIN = []

#Adding Function main()
def main():
    #Making Main() Not Create It's Own FILESADMIN
    global FILESADMIN
    
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

        #Mainking Function Terminal With Sudo, Terminal_prompt, Username Files_list. Can Be Used By: terminal(False, "Example Terminal User", "Example User", (FILESADMIN / FILESGUEST))
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
                        
                        #Checking If It Is Not Greater Then 1
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
                            
                            #Checking If Not
                            else:
                              #Printing Rm: Cannot Remove '{File_to_remove}': No Such File
                                print(f"rm: cannot remove '{file_to_remove}': No such file")
                        
                        #Checking If It Does Not Have A Second In Parts
                        else:
                            #Printing Rm: Missing Operand
                            print("rm: missing operand")

                    #Checking If Command = Sudo
                    elif command == "sudo":
                        #Printing: Usage: Sudo -H | -K | -K | -V
                        #          Usage: Sudo -V [-ABkNnS] [-G Group] [-H Host] [-P Prompt] [-U User]
                        #          Usage: Sudo -L [-ABkNnS] [-G Group] [-H Host] [-P Prompt] [-U User] [-U User]
                        #                     [Command [Arg ...]]
                        #          Usage: Sudo [-ABbEHkNnPS] [-R role] [-T Type] [-C Num] [-D Directory] [-G
                        #                      Group] [-H Host] [-P Prompt] [-R Directory] [-T Timeout] [-U User]
                        #
                        #          [VAR=Value] [-I | -S] [Command [Arg ...]]
                        #          Nusage: Sudo -E [-ABkNnS] [-R Role] [-T Type] [-C Num] [-D Directory] [-G Group]
                        #          [-H Host] [-P Prompt] [-R Directory] [-T Timeout] [-U User] File ...
                        print("usage: sudo -h | -K | -k | -V\nusage: sudo -v [-ABkNnS] [-g group] [-h host] [-p prompt] [-u user]\nusage: sudo -l [-ABkNnS] [-g group] [-h host] [-p prompt] [-U user] [-u user]\n            [command [arg ...]]\nusage: sudo [-ABbEHkNnPS] [-r role] [-t type] [-C num] [-D directory] [-g\n            group] [-h host] [-p prompt] [-R directory] [-T timeout] [-u user]\n[VAR=value] [-i | -s] [command [arg ...]]\nusage: sudo -e [-ABkNnS] [-r role] [-t type] [-C num] [-D directory] [-g group]\n[-h host] [-p prompt] [-R directory] [-T timeout] [-u user] file ...")

                            
            #Excepting An Keyboard Interruption
            except KeyboardInterrupt:

                #Printing:
                #         Returning to Main Menu...
                print("\nReturning to Main Menu...")
                
                #Returning To Main Menu
                return

        #Checking If Choice = 1
        if choice == "1":

            #Setting USER & PASS To An Input
            USER = input("user: ")
            PASS = input("pass: ")

            #Checking If USER = Arun C. & PASS = 927927
            if USER == "Arun C." and PASS == "927927":

                #Setting Admin_name To Admin
                admin_name = "Admin"

                #Runing Function Terminal With Data: True, {Admin_name}@{Hostname}:{Pwd} #, Admin_name, FILEADMIN
                terminal(True, f"{admin_name}@{hostname}:{pwd} # ", admin_name, FILESADMIN)
            
            #Checing If USER &/ PASS Is Not Arun C. / 927927
            else:

                #Printing:  ERROR: Invalid Credentials 
                print(" ERROR: Invalid Credentials ")

                #Exiting File

        #Checking If Choice = 2
        elif choice == "2":

            #Setting FILESGUEST To []
            FILESGUEST = []

            #Setting Guest_name To geust + int(100, 9999)
            guest_name = "guest" + str(random.randint(1000, 9999))

            #Runing Function Terminal With Data: False, {Guest_name}@{Hostname}:{Pwd} #, Guest_name, FILESGUEST
            terminal(False, f"{guest_name}@{hostname}:{pwd} $ ", guest_name, FILESGUEST)

        #Checking If Choice = 3
        elif choice == "3":

            #Printing Exiting...
            print("Exiting...")

            #Exiting File
            sys.exit()

    #Excepting An Keyboard Interruption
    except KeyboardInterrupt:

        #Printing Exiting Program...
        print("\nExiting Program...")

        #Exiting File
        sys.exit()

#Checking If __Name__ = __Main__
if __name__ == "__main__":

    #Runing Function Main
    main()
