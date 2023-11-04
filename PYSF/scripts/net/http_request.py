from lib import print_utils
from lib import var_util

INFO = {
    "name": "HTTP Request",
    "variables": ["URL", "METHOD"],
    "variables_description": ["The URL to send the request to", "The method to use"],
    "Variables_type": ["string", "string"],
    "variables_default": ["", "GET"],
    "variables_required": [True, False],
    "description": "Sends a HTTP request to a URL with the specified method",
    "requirements": ["requests"]
}

def main(variables):
    try:
        import requests
    except:
        print_utils.error("requests is not installed. Please install it with 'pip3 install requests'")
        return 1
    url = var_util.get_var_data(variables, "URL")
    method = var_util.get_var_data(variables, "METHOD")
    if method == None:
        method = "GET"
    try:
        print_utils.info(f"Sending {method} request to {url}")
        response = requests.request(method, url)
    except Exception as e:
        print_utils.error(f"Error sending request: {e}")
        return 1
    print_utils.success(f"Response Headers:\n{response.headers}")
    print_utils.success(f"Response Body:\n{response.text}")
    return 0