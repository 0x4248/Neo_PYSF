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
    for file in os.listdir(os.path.join(__MAIN__PATH, "scripts")):
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
    print("Welcome to PYSF!")
    print(f"Found {count_scripts()} scripts")
    command_line_message = "Neo PYSF (" + Fore.RED + "NO SCRIPT" + Style.RESET_ALL + ") > "
    script = None
    variables = []
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

            for root, dirs, files in os.walk(os.path.join(__MAIN__PATH, "scripts")):
                for file in files:
                    if file.endswith(".py"):
                        path = root.replace(os.path.join(__MAIN__PATH, "scripts"), "")
                        print(f"{path}/{file.replace('.py', '')}")

        elif entry.upper().startswith("USE"):
            try:
                script = entry.split(" ")[1]
            except IndexError:
                print_utils.error("Usage: USE <script>")
                continue
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

if __name__ == "__main__":
    main()