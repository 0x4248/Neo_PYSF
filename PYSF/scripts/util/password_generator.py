from lib import print_utils
from lib import var_util
import random
import string

INFO = {
    "name": "Password Generator",
    "variables": ["LENGTH", "COMPLEXITY"],
    "variables_description": ["The length of the password", "The complexity (easy, medium, hard)"],
    "Variables_type": ["int", "string"],
    "variables_default": [12, "medium"],
    "variables_required": [False, False],
    "description": "Generates a strong, random password",
    "requirements": []
}

def generate_password(length, complexity):
    if complexity == "easy":
        characters = string.ascii_letters
    elif complexity == "medium":
        characters = string.ascii_letters + string.digits
    elif complexity == "hard":
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = string.ascii_letters + string.digits

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main(variables):
    length = var_util.get_var_data(variables, "LENGTH")
    complexity = var_util.get_var_data(variables, "COMPLEXITY")

    if length is None:
        length = 12

    if complexity is None:
        complexity = "medium"

    password = generate_password(length, complexity)
    print_utils.success(f"Generated Password: {password}")
    return 0
