import logging
import config

def _create_logger_from_config():
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

logger = _create_logger_from_config()

