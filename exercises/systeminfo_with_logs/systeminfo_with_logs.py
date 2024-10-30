import platform
import socket
import os
import psutil
import argparse
import json
from logs import logger

"""
This script collects and displays various system information, including:
- Operating system details (version, hostname, and user)
- CPU usage statistics (count and usage percentage)
- Memory usage statistics (total, used, and free memory)
- List of currently running processes with relevant details

The user can specify which information to display using command-line arguments.
Additionally, the script supports output in both plain text and JSON formats.
"""

# Set up argparse for user input
parser = argparse.ArgumentParser(description="Script to gather system information")
parser.add_argument("-os", "--os-info", action='store_true', required=False, help="Display operating system info")
parser.add_argument("-c", "--cpu", action='store_true', required=False, help="Display CPU info")
parser.add_argument("-m", "--mem", action='store_true', required=False, help="Display memory info")
parser.add_argument("-p", "--proc", action='store_true', required=False, help="Display process info")
parser.add_argument("-a", "--all", action='store_true', required=False, help="Display all info")
parser.add_argument("-f", "--format", choices=["text", "json"], default="text", help="Output format: text or json")
args = parser.parse_args()

args_list = vars(args) # converts args to dictionary example: {'os_info': True, 'cpu': False, 'mem': True, 'proc': False, 'all': False, 'format': 'text'}

class SystemInfo:
    def __init__(self):
        self.result = {
            "os_info": {},
            "cpu": {},
            "mem": {}
        }
        logger.debug(f'SystemInfo object created')

    def get_os_info(self):
        """Collect operating system information."""
        logger.debug(f'Getting OS info')
        try:
            self.result['os_info'] = {
                "Operating System": platform.system(),
                "Hostname": socket.gethostname(),
                "User": os.getlogin()
            }
        except Exception as e:
            logger.error(f"Could not retrieve OS info: {str(e)}")
            self.result['os_info'] = {"Error": f"Could not retrieve OS info: {str(e)}"}

    def get_cpu_info(self):
        """Collect CPU usage information."""
        logger.debug(f'Getting CPU info')
        try:
            self.result['cpu'] = {
                "Count": psutil.cpu_count(logical=True),
                "Usage": f"{psutil.cpu_percent(interval=1)}%"
            }
        except Exception as e:
            logger.error(f"Could not retrieve CPU info: {str(e)}")
            self.result['cpu'] = {"Error": f"Could not retrieve CPU info: {str(e)}"}

    def get_memory_info(self):
        """Collect memory usage information."""
        logger.debug(f'Getting memory info')
        try:
            mem = psutil.virtual_memory()
            self.result['mem'] = {
                "Total Memory (GB)": round(mem.total / (1024 ** 3), 2),
                "Used Memory (GB)": round(mem.used / (1024 ** 3), 2),
                "Free Memory (GB)": round(mem.free / (1024 ** 3), 2)
            }
        except Exception as e:
            logger.error(f"Could not retrieve memory info: {str(e)}")
            self.result['mem'] = {"Error": f"Could not retrieve memory info: {str(e)}"}

    def collect_info(self):
        """Gather the specified system information."""
        self.get_os_info()
        self.get_cpu_info()
        self.get_memory_info()

    def display_result(self, metrics, format="text"):
        """Display collected information in the specified format."""
        logger.debug(f'Displaying result')
        response = {}
        if 'all' in metrics:
            response = self.result
        else:
            for metric in metrics:
                response[metric] = self.result[metric]
        
        if format == "json":
            logger.debug(f'Output format: JSON')
            print(json.dumps(response, indent=4))
        else:
            logger.debug(f'Output format: text')
            for key in response:
                print(f'{key}:')
                print(str(response[key]).strip('{}').replace(',', '\n'))

no_args = True
for arg in args_list:
    if args_list[arg] == True:
        no_args = False

if no_args:
    logger.debug(f'Arguments provided: {args_list}')
    raise Exception('NoArgumentsException', 'No information requested. Use -h or --help for available options.')

# Initialize SystemInfo instance
system_info = SystemInfo()
# Collect specified information
system_info.collect_info()
args_list = vars(args)
args_to_display = []

if args_list['all']:
    args_to_display.append("all")
else:
    for arg in args_list:
        if args_list[arg] == True:
            args_to_display.append(arg)

# Display the collected information
system_info.display_result(args_to_display, args.format)

