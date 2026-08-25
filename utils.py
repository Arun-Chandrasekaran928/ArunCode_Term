import sys
import os
import tty
import termios

def get_masked_input(prompt=""):
    """Reads characters one by one and prints asterisks for masked inputs."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    password = ""
    try:
        tty.setraw(sys.stdin.fileno())
        while True:
            ch = sys.stdin.read(1)
            if ch == '\r' or ch == '\n':
                sys.stdout.write('\r\n')
                break
            elif ch == '\x7f':
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            elif ch == '\x03':
                raise KeyboardInterrupt
            else:
                password += ch
                sys.stdout.write('*')
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
    return password

def run_real_nano(file_path, filename):
    """Simulates a full-screen text editor interface matching GNU nano."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    lines = [""]
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read()
            if content:
                lines = content.splitlines()
    if not lines:
        lines = [""]

    cur_line = len(lines) - 1
    
    def refresh_screen():
        sys.stdout.write('\033[H\033[2J')
        sys.stdout.write(f"\033[7m  GNU nano 4.8              File: {filename}                            \033[0m\r\n\n")
        for idx, line in enumerate(lines):
            if idx == cur_line:
                sys.stdout.write(line + "█\r\n")
            else:
                sys.stdout.write(line + "\r\n")
        
        sys.stdout.write("\n" * (15 - len(lines)))
        sys.stdout.write("\033[7m^G\033[0m Get Help  \033[7m^O\033[0m Write Out \033[7m^R\033[0m Read File \033[7m^Y\033[0m Prev Page \033[7m^K\033[0m Cut Text  \033[7m^C\033[0m Cur Pos\r\n")
        sys.stdout.write("\033[7m^X\033[0m Exit      \033[7m^J\033[0m Justify   \033[7m^W\033[0m Where Is  \033[7m^V\033[0m Next Page \033[7m^U\033[0m Uncut Text\033[7m^T\033[0m To Spell\r\n")
        sys.stdout.flush()

    try:
        tty.setraw(fd)
        while True:
            refresh_screen()
            ch = sys.stdin.read(1)
            
            if ch == '\x18':  # Ctrl+X
                sys.stdout.write('\033[H\033[2J')
                break
            elif ch == '\x0f':  # Ctrl+O
                with open(file_path, "w") as f:
                    f.write("\n".join(lines))
            elif ch == '\r' or ch == '\n':
                lines.insert(cur_line + 1, "")
                cur_line += 1
            elif ch == '\x7f':
                if len(lines[cur_line]) > 0:
                    lines[cur_line] = lines[cur_line][:-1]
                elif cur_line > 0:
                    old_line_content = lines.pop(cur_line)
                    cur_line -= 1
                    lines[cur_line] += old_line_content
            else:
                if ord(ch) >= 32:
                    lines[cur_line] += ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
