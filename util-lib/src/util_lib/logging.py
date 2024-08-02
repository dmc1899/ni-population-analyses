import logging
import sys


def configure_logging(level=logging.DEBUG, log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    """
    Configure the logging settings
    """
    logging.basicConfig(level=level, format=log_format, handlers=[logging.StreamHandler(sys.stdout)]
)