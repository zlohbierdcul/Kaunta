import logging
import sys
from discord.utils import setup_logging
from discord.utils import MISSING


handler = MISSING
formatter = MISSING
level = MISSING
setup_logging(handler=handler, formatter=formatter, level=level)

def get_logger(file):
    logger = logging.getLogger(file)
    return logger