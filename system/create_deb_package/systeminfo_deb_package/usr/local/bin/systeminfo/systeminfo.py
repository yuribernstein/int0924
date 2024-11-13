import platform
import socket
import os
import psutil
import json

class SystemInfo:
    def __init__(self):
        self.result = {
            "os_info": {},
            "cpu": {},
            "mem": {}
            # "proc": []
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

    # def get_process_info(self):
    #     """Collect information on running processes."""
    #     try:
    #         self.result['proc'] = [
    #             proc.info for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent'])
    #         ]
    #     except Exception as e:
    #         self.result['proc'] = {"Error": f"Could not retrieve process info: {str(e)}"}

    def collect_info(self):
        """Gather all system information."""
        self.get_os_info()
        self.get_cpu_info()
        self.get_memory_info()
        # self.get_process_info()

    def display_result(self, metrics, format="text"):
        """Return collected information in the specified format."""
        response = {}
        
        if 'all' in metrics:
            response = self.result
        else:
            for metric in metrics:
                response[metric] = self.result.get(metric, {})

        if format == "json":
            return response  # Return data as JSON-compatible dictionary
        else:
            # Convert dictionary to a formatted text response
            text_output = ""
            for key, value in response.items():
                text_output += f'{key}:\n'
                for subkey, subvalue in value.items():
                    text_output += f"  {subkey}: {subvalue}\n"
            return text_output.strip()  # Return formatted text
