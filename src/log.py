import logging

logging.basicConfig(level=logging.DEBUG)

def get_logger(name):
    return logging.getLogger(name)

