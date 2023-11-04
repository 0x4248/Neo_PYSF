from lib import print_utils
from lib import var_util
import socket

INFO = {
    "name": "Port Scanner",
    "variables": ["TARGET_HOST", "START_PORT", "END_PORT"],
    "variables_description": ["The target host to scan", "The starting port for the scan", "The ending port for the scan"],
    "Variables_type": ["string", "int", "int"],
    "variables_default": ["localhost", 1, 100],
    "variables_required": [True, False, False],
    "description": "Scans open ports on a target host within a specified port range",
    "requirements": []
}

def main(variables):
    target_host = var_util.get_var_data(variables, "TARGET_HOST")
    start_port = var_util.get_var_data(variables, "START_PORT")
    end_port = var_util.get_var_data(variables, "END_PORT")

    if not target_host:
        print_utils.error("TARGET_HOST is a required variable.")
        return 1

    if not start_port or not end_port:
        print_utils.error("START_PORT and END_PORT are required variables.")
        return 1

    open_ports = []
    try:
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
    except Exception as e:
        print_utils.error(f"Error scanning ports: {e}")
        return 1

    if open_ports:
        print_utils.success(f"Open ports on {target_host}: {open_ports}")
    else:
        print_utils.success(f"No open ports found on {target_host}")
    
    return 0
