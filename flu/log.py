# coding=utf-8

import sys
import logging
from flask import app

def setup_logger(name):
    manager = logging.Logger.manager
    logger_created = name in manager.loggerDict
    logger = logging.getLogger(name)
    if app.get_debug_flag():
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if not logger_created:
        default_handler = logging.StreamHandler(sys.stderr)
        default_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
        ))
        logger.addHandler(default_handler)
    return logger

