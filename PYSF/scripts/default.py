from lib import print_utils
from lib import var_util

INFO = {
    "name": "default",
    "variables": ["NAME"],
    "variables_description": ["The name to print"],
    "Variables_type": ["string"],
    "variables_default": ["Neo"],
    "variables_required": [False],
    "description": "Example script for Neo PYSF that takes in a name and prints it with hello",
    "requirements": []
}

def main(variables):
    name = var_util.get_var_data(variables, "NAME")
    if name == None:
        name = "Neo"
    print_utils.success(f"Hello {name}!")
    return 0