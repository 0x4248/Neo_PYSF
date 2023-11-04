from lib import print_utils
from lib import var_util

INFO = {
    "name": "String to binary",
    "variables": ["STRING", "SPLIT"],
    "variables_description": ["The string to convert to binary", "The character to split the binary with"],
    "Variables_type": ["string", "string"],
    "variables_default": ["", ""],
    "variables_required": [True, False],
    "description": "Converts a string to binary and prints it",
    "requirements": []
}

def main(variables):
    string = var_util.get_var_data(variables, "STRING")
    split = var_util.get_var_data(variables, "SPLIT")
    if split == None:
        split = ""
    print_utils.success(split.join(format(ord(x), 'b') for x in string))
    return 0