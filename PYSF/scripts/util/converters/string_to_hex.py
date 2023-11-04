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
    string = var_util.get_var_data(variables, "STRING")
    print_utils.success(string.encode().hex())
    return 0