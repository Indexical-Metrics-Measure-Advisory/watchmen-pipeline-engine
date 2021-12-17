import logging
import logging.handlers
import sys

from pipeline.config.config import PROD, settings


def init():
    logging.getLogger().setLevel(logging.NOTSET)

    # Add stdout handler, with level INFO
    console = logging.StreamHandler(sys.stdout)
    if settings.ENVIRONMENT == PROD:
        console.setLevel(logging.ERROR)
    else:
        console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-13s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)



    # return logging

# log = logging.getLogger("app." + __name__)
#
# log.debug('Debug message, should only appear in the file.')
# log.info('Info message, should appear in file and stdout.')
# log.warning('Warning message, should appear in file and stdout.   ')
# log.error('Error message, should appear in file and stdout.')
