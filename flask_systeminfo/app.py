import logging
import sys
from flask import Flask, request, jsonify, render_template
from systeminfo import SystemInfo

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(filename)s:%(lineno)d, Function: %(funcName)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("flask.systeminfo.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize SystemInfo instance
system_info = SystemInfo()

@app.route('/systeminfo', methods=['GET'])
def systeminfo():
    """
    Route to fetch system information in text format based on 'metric' query parameter.
    Expected values for 'metric': os_info, cpu, mem, proc, all.
    """
    metric = request.args.get('metric', default=None)
    
    if metric not in ['os_info', 'cpu', 'mem', 'all']:
        logger.error("Invalid metric requested")
        return "Invalid metric. Expected one of: os_info, cpu, mem, all", 400

    # Collect system info
    system_info.collect_info()
    output = system_info.display_result([metric], format="text")

    logger.info(f"System info for {metric} retrieved successfully.")
    return output

@app.route('/systeminfo/json', methods=['GET'])
def systeminfo_json():
    """
    Route to fetch all system information in JSON format.
    """
    # Collect system info
    system_info.collect_info()
    output = system_info.display_result(['all'], format="json")

    logger.info("System info (JSON format) retrieved successfully.")
    return jsonify(output)

@app.route('/<filename>')
def static_file(filename):
    return app.send_static_file(filename)

@app.route('/')
def index():
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(port=8080)
