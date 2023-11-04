from lib import print_utils
from lib import var_util

INFO = {
    "name": "Hex to String",
    "variables": ["STRING"],
    "variables_description": ["The hex string to convert"],
    "Variables_type": ["string"],
    "variables_default": [""],
    "variables_required": [True],
    "description": "Converts a hex string to a string",
    "requirements": []
}

def main(variables):
    string = var_util.get_var_data(variables, "STRING")
    if string == None:
        print_utils.error("No string provided")
        return 1
    try:
        print(bytes.fromhex(string).decode('utf-8'))
    except:
        print_utils.error("Invalid hex string")
        return 1
    return 0