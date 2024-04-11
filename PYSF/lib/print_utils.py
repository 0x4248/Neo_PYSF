# Neo PYSF
# The new version of PYSF. A metasploit-like framework but for python scripts instead of exploits.
# GitHub: https://www.github.com/0x4248/Neo_PYSF
# License: GNU General Public License v3.0
# By: 0x4248

from colorama import Fore, Style

def log(msg):
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {msg}")

def info(msg):
    print(f"{Fore.BLUE}[i]{Style.RESET_ALL} {msg}")

def warn(msg):
    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {msg}")

def error(msg):
    print(f"{Fore.RED}[-]{Style.RESET_ALL} {msg}")

def success(msg):
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {msg}")

def question(msg):
    print(f"{Fore.YELLOW}[?]{Style.RESET_ALL} {msg}")

def debug(msg):
    print(f"{Fore.MAGENTA}[D]{Style.RESET_ALL} {msg}")

def fatal(msg):
    print(f"{Fore.RED}[X]{Style.RESET_ALL} {msg}")

def banner():
    print(f"""{Fore.CYAN}
  _   _              _______     _______ ______ 
 | \ | |            |  __ \ \   / / ____|  ____|
 |  \| | ___  ___   | |__) \ \_/ / (___ | |__   
 | . ` |/ _ \/ _ \  |  ___/ \   / \___ \|  __|  
 | |\  |  __/ (_) | | |      | |  ____) | |     
 |_| \_|\___|\___/  |_|      |_| |_____/|_|     
{Style.RESET_ALL}""")
                                                