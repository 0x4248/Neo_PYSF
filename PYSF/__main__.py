# Neo PYSF
# The new version of PYSF. A metasploit-like framework but for python scripts instead of exploits.
# GitHub: https://www.github.com/lewisevans2007/Neo_PYSF
# License: GNU General Public License v3.0
# By: Lewis Evans

import importlib
import sys
import os
from colorama import Fore, Style

from lib import print_utils

__MAIN__PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__MAIN__PATH)

def count_scripts():
    x = 0
    for root, dirs, files in os.walk(os.path.join(__MAIN__PATH, "scripts")):
        for file in files:
            if file.endswith(".py"):
                x += 1
    return x

def convert_script_to_py_path(script):
    """
    Turns a script path that is entered by the user into a python path
    e.g. util/ping -> scripts.util.ping
    """
    script = script.replace("/", ".")
    return f"scripts.{script}"

def main():
    print_utils.banner()
    print("Welcome to Neo PYSF!")
    print("Found "+ Fore.BLUE + str(count_scripts()) + Style.RESET_ALL + " scripts")
    command_line_message = "Neo PYSF (" + Fore.RED + "NO SCRIPT" + Style.RESET_ALL + ") > "
    script = None
    variables = []
    recent_scan_results = []
    while True:
        entry = input(command_line_message)
        if entry.upper() == "EXIT" or entry.upper() == "QUIT" or entry.upper() == "Q" or entry.upper() == "E":
            sys.exit(0)
        elif entry == "":
            continue
        
        elif entry.upper().startswith("SET"):
            try:
                variable_name = entry.split(" ")[1].upper()
                variable_value = entry.split(" ")[2]
                variable_exists = False
            except IndexError:
                print_utils.error("Usage: SET <variable_name> <variable_value>")
                continue
            for variable in variables:
                if variable[0] == variable_name:
                    variable_exists = True
                    variable[1] = variable_value
                    break
            if not variable_exists:
                variables.append([variable_name, variable_value])
            print_utils.success(f"SET {variable_name} => {variable_value}")

        elif entry.upper().startswith("PRINTVARS") or entry.upper().startswith("PV"):
            if len(variables) == 0:
                print_utils.warn("No variables to print")
                continue
            print_utils.info("Printing variables")
            for variable in variables:
                if variable[1].count(".") == 3:
                    print(f"{Fore.GREEN}{variable[0]}{Style.RESET_ALL} => {Fore.GREEN}{variable[1]}{Style.RESET_ALL}")
                elif variable[1].isdigit():
                    print(f"{Fore.BLUE}{variable[0]}{Style.RESET_ALL} => {Fore.BLUE}{variable[1]}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}{variable[0]}{Style.RESET_ALL} => {Fore.YELLOW}{variable[1]}{Style.RESET_ALL}")

        elif entry.upper().startswith("CLEARVARS") or entry.upper().startswith("CV"):
            if len(variables) == 0:
                print_utils.warn("No variables to clear")
                continue
            print_utils.info("Clearing variables")
            variables = []

        elif entry.upper().startswith("LIST"):
            x = 0
            recent_scan_results = []
            for root, dirs, files in os.walk(os.path.join(__MAIN__PATH, "scripts")):
                for file in files:
                    if file.endswith(".py"):
                        path = root.replace(os.path.join(__MAIN__PATH, "scripts"), "")
                        if path.startswith("/"):
                            path = path[1:]
                        print(f"{Fore.CYAN}{x}{Style.RESET_ALL} {path}/{file.replace('.py', '')}")
                        x += 1
                        recent_scan_results.append(f"{path}/{file.replace('.py', '')}")

        elif entry.upper().startswith("USE"):
            try:
                script = entry.split(" ")[1]
            except IndexError:
                print_utils.error("Usage: USE <script>")
                continue
            # if number like set 1 select the 2nd item in recent_scan_results if there are items
            if script.isdigit() and len(recent_scan_results) > 0:
                script = recent_scan_results[int(script)]
            script_path = convert_script_to_py_path(script)
            try:
                script_module = importlib.import_module(script_path)
            except ModuleNotFoundError:
                print_utils.error(f"Script {script} not found or cant import required modules")
                continue
            except Exception as e:
                print_utils.error(f"Error loading script {script}: {e}")
                continue
            print_utils.success(f"Loaded script {script}")
            command_line_message = "Neo PYSF (" + Fore.GREEN + script + Style.RESET_ALL + ") > "

        elif entry.upper().startswith("RUN"):
            error_occured = False
            if script is None:
                print_utils.error("No script loaded")
                continue
            try:
                info = script_module.INFO
                if len(variables) == 0 and True in info["variables_required"]:
                    print_utils.error("No variables set")
                    error_occured = True
                elif len(variables) == 0 and True not in info["variables_required"]:
                    pass
                else:
                    for i in range(len(info["variables"])):
                        variable_name = info["variables"][i]
                        variable_type = info["Variables_type"][i]
                        variable_required = info["variables_required"][i]
                        variable_default = info["variables_default"][i]
                        variable_current_value = None
                        if True in info["variables_required"]:
                            for variable in variables:
                                if variable[0] == variable_name:
                                    variable_current_value = variable[1]
                                    break
                            if variable_required and variable_current_value == None:
                                print_utils.error(f"Variable {variable_name} is required")
                                error_occured = True
                if error_occured == True:
                    continue    
                else:
                    ret = script_module.main(variables)
            except Exception as e:
                print_utils.error(f"Error running script {script}: {e}")
                continue
            if ret == 0:
                continue
            elif ret == None:
                print_utils.info(f"Script {script} returned" + Fore.BLUE + " None" + Style.RESET_ALL)
            else:
                print_utils.info(f"Script {script} returned" + Fore.BLUE + f" {ret}" + Style.RESET_ALL)
                
        elif entry.upper().startswith("INFO"):
            if script is None:
                print_utils.error("No script loaded")
                continue
            try:
                info = script_module.INFO
            except Exception as e:
                print_utils.error(f"Error reading INFO from script {script}: {e}")
                continue
            print_utils.info(f"Name: {info['name']}")
            print_utils.info(f"Description: {info['description']}")
            print_utils.info("Variables:")
            print("\tNAME\tTYPE\tREQUIRED\tDEFAULT\tCURRENT VALUE (if set)")
            for i in range(len(info["variables"])):
                variable_name = info["variables"][i]
                variable_type = info["Variables_type"][i]
                variable_required = info["variables_required"][i]
                variable_default = info["variables_default"][i]
                variable_current_value = None
                for variable in variables:
                    if variable[0] == variable_name:
                        variable_current_value = variable[1]
                        break
                print(f"\t{variable_name}\t{variable_type}\t{variable_required}\t\t{variable_default}\t{variable_current_value}")
            print_utils.info("Variables Description:")
            for i in range(len(info["variables"])):
                variable_name = info["variables"][i]
                variable_description = info["variables_description"][i]
                print(f"\t{variable_name}\t{variable_description}")
            print_utils.info("Requirements:")
            for requirement in info["requirements"]:
                print(f"\t{requirement}")
        elif entry.upper().startswith("HELP"):
            print_utils.info("Neo PYSF Help")
            print_utils.info("Commands:")
            print("\tSET <variable_name> <variable_value>\tSets a variable")
            print("\tPRINTVARS (PV)\t\t\t\tPrints all variables")
            print("\tCLEARVARS (CV)\t\t\t\tClears all variables")
            print("\tLIST\t\t\t\t\tLists all scripts")
            print("\tUSE <script>\t\t\t\tLoads a script")
            print("\tRUN\t\t\t\t\tRuns the loaded script")
            print("\tINFO\t\t\t\t\tDisplays info about the loaded script")
            print("\tSEARCH\t\t\t\t\tSearches for a script")
            print("\tHELP\t\t\t\t\tDisplays this help message")
            print("\tEXIT (QUIT, Q, E)\t\t\tExits Neo PYSF")
        elif entry.upper().startswith("SEARCH"):
            try:
                search_term = entry.split(" ")[1]
            except IndexError:
                print_utils.error("Usage: SEARCH <search_term>")
                continue
            found = False
            x = 0
            recent_scan_results = []
            for root, dirs, files in os.walk(os.path.join(__MAIN__PATH, "scripts")):
                for file in files:
                    if file.endswith(".py"):
                        path = root.replace(os.path.join(__MAIN__PATH, "scripts"), "")
                        if search_term in path or search_term in file.replace(".py", ""):
                            if path.startswith("/"):
                                path = path[1:]
                            print(f"{Fore.CYAN}{x}{Style.RESET_ALL} {path.replace(search_term, Fore.RED + search_term + Style.RESET_ALL)}/{file.replace('.py', '').replace(search_term, Fore.RED + search_term + Style.RESET_ALL)}")
                            found = True
                            x += 1
                            recent_scan_results.append(f"{path}/{file.replace('.py', '')}")
            if not found:
                print_utils.warn("No scripts found")

if __name__ == "__main__":
    main()