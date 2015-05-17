from __future__ import unicode_literals
import os
import time
import logging

import requests

import kvaut.errors


RETRIES=6
TIMEOUT=3

def assert_is_visible(target):
    raise kvaut.errors.AssertionError("Fail")

def wait_for_automation_server():
    logger.info('waiting for automation server')

    def automation_server_exists():
        try:
            response = requests.get("http://0.0.0.0:5123/ping", timeout=TIMEOUT)
            return response.status_code == 200
        except Exception as ex:
            logger.debug('error occurred while waiting for automation server: {}'.format(ex))
            return False

    if not wait_for(automation_server_exists):
        raise kvaut.errors.ServerNotFoundError('kvaut timed out waiting for automation server')

def wait_for(condition, retries=RETRIES, loop_delay=0.5):
    met_condition = False
    retry_count = 0
    while (retry_count < retries and not met_condition):
        retry_count += 1
        time.sleep(loop_delay)
        met_condition = condition()

    return met_condition

log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
}
log_level_name = os.environ.get('KVAUT_LOG', 'ERROR')
logging.basicConfig(level=log_levels[log_level_name])
logger = logging.getLogger(__name__)
logger.setLevel(log_levels[log_level_name])
logger.info('kvaut log level is {}'.format(log_level_name))
