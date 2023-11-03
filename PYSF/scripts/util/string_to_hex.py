from lib import print_utils
from lib import var_util

INFO = {
    "name": "String to Hex",
    "variables": ["STRING"],
    "variables_description": ["The string to convert to hex"],
    "Variables_type": ["string"],
    "variables_default": [""],
    "variables_required": [True],
    "description": "Converts a string to hex and prints it",
    "requirements": []
}

def main(variables):
    string = variables[0][1]
    print_utils.success(string.encode().hex())
    return 0