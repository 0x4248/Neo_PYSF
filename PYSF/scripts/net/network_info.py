from lib import print_utils
from lib import var_util
import psutil
import socket

INFO = {
    "name": "Network Information",
    "variables": [],
    "variables_description": [],
    "Variables_type": [],
    "variables_default": [],
    "variables_required": [],
    "description": "Retrieves and displays network-related information about the system",
    "requirements": ["psutil"]
}

def main(variables):
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    
    network_info = {
        "Host Name": host_name,
        "IP Address": ip_address,
        "Network Interfaces": list(psutil.net_if_addrs().keys())
    }

    print_utils.success("Network Information:")
    for key, value in network_info.items():
        print_utils.success(f"{key}: {value}")

    return 0
