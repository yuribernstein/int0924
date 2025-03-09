import time
import functools

class Utils():
    def __init__(self):
        from logs import logger
        self.logger = logger
    
    def retry_this(self, retries=3, delay=1, backoff=1.5, exceptions=(Exception,)): # retry X times with Y delay in between and Z time between each retry
        def decorator_retry(func):
            @functools.wraps(func)
            def wrapper_retry(*args, **kwargs):
                _retries, _delay = retries, delay
                while _retries > 0:
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        _retries -= 1
                        if _retries == 0:
                            self.logger.error(f"Function {func.__name__} failed after {retries} retries.")
                            raise
                        else:
                            self.logger.warning(f"Retrying {func.__name__} in {_delay} seconds due to {e}... {_retries} retries left.")
                            time.sleep(_delay)
                            _delay *= backoff
            return wrapper_retry
        return decorator_retry   


    def measure_this(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()  # Record the start time
            result = func(*args, **kwargs)  # Execute the function
            end_time = time.time()  # Record the end time
            execution_time = end_time - start_time  # Calculate the elapsed time
            self.logger.info(f"EXECUTION TIME FOR {func.__name__}: {execution_time:.4f} SECONDS")  
                          
            return result  # Return the original result
            
        return wrapper
    
    
    def singleton(self, cls):
        instances = {}

        @functools.wraps(cls)
        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        
        return get_instance