import sys
if sys.version_info < (3, 6, 5):
    sys.exit('GomerX SDK requires Python 3.6.5 or later')

import logging
import time

logger_name = 'gomerx'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.WARN)
