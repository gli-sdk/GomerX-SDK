import sys
if sys.version_info < (3, 6, 5):
    sys.exit('GomerX SDK requires Python 3.6.5 or later')

import logging
import time

logger_name = 'gomerx'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

logger.info("***** Welcome to the world of GomerX. Just enjoy it! *****")


__all__ = ['logger', 'protocol', 'config', 'version', 'action', 'connection', 'client',
           'module', 'robot', 'chassis', 'gripper',  'camera', 'led', 'arm', 'skill']
