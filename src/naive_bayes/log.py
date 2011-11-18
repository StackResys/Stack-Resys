""" This module provides a globally accessible
    logger created from the config file """

import logging
import config

def _create_logger_from_config():
    """ Create the logger from the config file """
    conf = config.LOGGER
    logging.basicConfig(format=conf["format"])
    logger = logging.getLogger(conf["name"])

    # if need to write to the log file
    if conf['log_file'] is not None:
        handler = logging.FileHandler(conf['log_file'])
        logger.addHandler(handler)

    logger.setLevel(conf["level"])
    logger.debug("Logger initialized")

    return logger

LOGGER = _create_logger_from_config()

