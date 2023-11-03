# Neo PYSF
# The new version of PYSF. A metasploit-like framework but for python scripts instead of exploits.
# GitHub: https://www.github.com/lewisevans2007/Neo_PYSF
# License: GNU General Public License v3.0
# By: Lewis Evans

def get_var_data(variables, var_name):
    for variable in variables:
        if variable[0] == var_name:
            return variable[1]
    return None