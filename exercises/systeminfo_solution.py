import platform
import socket
import os
import psutil
import argparse
import json

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
            "mem": {},
            "proc": []
        }

    def get_os_info(self):
        """Collect operating system information."""
        try:
            self.result['os_info'] = {
                "Operating System": platform.system(),
                "Hostname": socket.gethostname(),
                "User": os.getlogin()
            }
        except Exception as e:
            self.result['os_info'] = {"Error": f"Could not retrieve OS info: {str(e)}"}

    def get_cpu_info(self):
        """Collect CPU usage information."""
        try:
            self.result['cpu'] = {
                "Count": psutil.cpu_count(logical=True),
                "Usage": f"{psutil.cpu_percent(interval=1)}%"
            }
        except Exception as e:
            self.result['cpu'] = {"Error": f"Could not retrieve CPU info: {str(e)}"}

    def get_memory_info(self):
        """Collect memory usage information."""
        try:
            mem = psutil.virtual_memory()
            self.result['mem'] = {
                "Total Memory (GB)": round(mem.total / (1024 ** 3), 2),
                "Used Memory (GB)": round(mem.used / (1024 ** 3), 2),
                "Free Memory (GB)": round(mem.free / (1024 ** 3), 2)
            }
        except Exception as e:
            self.result['mem'] = {"Error": f"Could not retrieve memory info: {str(e)}"}

    def get_process_info(self):
        """Collect information on running processes."""
        try:
            self.result['proc'] = [
                proc.info for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent'])
            ]
        except Exception as e:
            self.result['proc'] = {"Error": f"Could not retrieve process info: {str(e)}"}

    def collect_info(self):
        """Gather the specified system information."""
        self.get_os_info()
        self.get_cpu_info()
        self.get_memory_info()
        self.get_process_info()

    def display_result(self, metrics, format="text"):
        """Display collected information in the specified format."""
        response = {}
        if 'all' in metrics:
            response = self.result
        else:
            for metric in metrics:
                response[metric] = self.result[metric]
        
        if format == "json":
            print(json.dumps(response, indent=4))
        else:
            for key in response:
                print(f'{key}:')
                print(str(response[key]).strip('{}').replace(',', '\n'))


# Initialize SystemInfo instance
system_info = SystemInfo()

# Collect specified information
system_info.collect_info()

# print a message if no information was requested
if all(arg is False for arg in args_list) and not args.all:
    print("No information requested. Use -h or --help for available options.")
    exit()

args_to_display = []

if args_list['all']:
    args_to_display.append("all")
else:
    for arg in args_list:
        if args_list[arg] == True:
            args_to_display.append(arg)

# Display the collected information
system_info.display_result(args_to_display, args.format)

