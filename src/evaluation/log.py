""" This module provides a globally accessible
    logger created from the config file """

import logging

def _create_logger_from_config():
    """ Create the logger from the config file """
    conf = {
        "name": "StackLogger",
        "log_file": "logs/experiment.log",
        "format": "%(asctime)s %(levelname)s \n  >>> %(message)s",
        "level": logging.DEBUG
    }

    logging.basicConfig(format=conf["format"])
    logger = logging.getLogger(conf["name"])

    # if need to write to the log file
    log_file = conf['log_file']
    if log_file is not None:
        handler = logging.FileHandler(conf['log_file'])
        logger.addHandler(handler)

    logger.setLevel(conf["level"])
    logger.debug("Logger initialized")

    return logger

LOGGER = _create_logger_from_config()

