import logging
import sys

    

logging.basicConfig(level=logging.DEBUG, 
                    format='[%(asctime)s - %(filename)s:%(lineno)d, Function: %(funcName)s] %(levelname)s - %(message)s', 
                    handlers=[
                        logging.FileHandler("./logs/systeminfo.log"),
                        logging.StreamHandler(sys.stdout)
                    ]
)

logger = logging.getLogger(__file__)
