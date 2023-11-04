from lib import print_utils
from lib import var_util

INFO = {
    "name": "File Downloader",
    "variables": ["URL", "SAVE_PATH"],
    "variables_description": ["The URL of the file to download", "The local path to save the file"],
    "Variables_type": ["string", "string"],
    "variables_default": ["", ""],
    "variables_required": [True, True],
    "description": "Downloads a file from a URL to a local directory",
    "requirements": ["requests"]
}

def main(variables):
    try:
        import requests
    except:
        print_utils.error("requests is not installed. Please install it with 'pip3 install requests'")
        return 1
    url = var_util.get_var_data(variables, "URL")
    save_path = var_util.get_var_data(variables, "SAVE_PATH")
    if not url or not save_path:
        print_utils.error("URL and SAVE_PATH are required variables.")
        return 1
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print_utils.error(f"Error downloading file: {e}")
        return 1

    with open(save_path, 'wb') as file:
        file.write(response.content)
        print_utils.success(f"File downloaded and saved to {save_path}")
    return 0
