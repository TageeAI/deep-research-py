import logging
import datetime
import os
# Configure logging

def initial_logger(logging_path: str = "log", enable_stdout: bool = False) -> None:
    """Initializes the logger for the application."""
    global logger

    now = datetime.datetime.now()
    log_file = os.path.join(
        logging_path, f"deep_research_py_{now.strftime('%Y%m%d_%H%M%S')}.log"
    )
    if not os.path.exists(logging_path):
        os.makedirs(logging_path)

    # Set up logging to stdout if enabled
    handlers = [logging.FileHandler(log_file, encoding='utf-8')]
    if enable_stdout:
        handlers.append(logging.StreamHandler())
    # Set up logging to a file
    logging.basicConfig(
        encoding='utf-8',
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=handlers
    )
    logger = logging.getLogger("deep_research_py")
    logger.setLevel(logging.INFO)
    return logger
    
logger = initial_logger()
