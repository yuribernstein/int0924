import logging
import sys
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    

logging.basicConfig(level=logging.DEBUG, 
                    format='[%(asctime)s - %(filename)s:%(lineno)d, Function: %(funcName)s] %(levelname)s - %(message)s', 
                    handlers=[
                        logging.FileHandler("/tmp/runtime.log"),
                        logging.StreamHandler(sys.stdout)
                    ]
)

logger = logging.getLogger(__file__)
