from __future__ import unicode_literals
import os
import time
import json
import logging

import requests

from kvaut.helpers.wait import *
import kvaut.errors


JSON_HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json' }
SERVER="http://0.0.0.0:5155"
TIMEOUT=3

def assert_is_visible(target):
    if not wait_for(lambda: find_element(target)):
        raise kvaut.errors.AssertionError('Could not find element matching \"{}\"'.format(target))

def find_element(target):
    found_element = None

    try:
        body = {'query':{'value':target }}
        response = requests.post(url_for('/find_element'), data=json.dumps(body), headers=JSON_HEADERS, timeout=TIMEOUT)
        found_element = response.json()
        if len(found_element.keys()) == 0:
            found_element = None
    except Exception as ex:
        logger.debug('error occurred attempting to find element matching \"{}\": {}'.format(target, ex))

    print("found element {}".format(found_element))
    return found_element

def tap(target):
    assert_is_visible(target)

    tapped_element = None
    try:
        body = {'query':{'value':target }}
        response = requests.post(url_for('/tap'), data=json.dumps(body), headers=JSON_HEADERS, timeout=TIMEOUT)
        tapped_element = response.json()
        if len(tapped_element.keys()) == 0:
            tapped_element = None
    except Exception as ex:
        logger.debug('error occurred attempting to tap element matching \"{}\": {}'.format(target, ex))

    print("tapped element {}".format(tapped_element))
    return tapped_element

def wait_for_automation_server():
    logger.info('waiting for automation server')

    def automation_server_exists():
        try:
            response = requests.get(url_for("/ping"), timeout=TIMEOUT)
            return response.status_code == 200
        except Exception as ex:
            logger.debug('error occurred while waiting for automation server: {}'.format(ex))
            return False

    if not wait_for(automation_server_exists):
        raise kvaut.errors.ServerNotFoundError('kvaut timed out waiting for automation server')

def url_for(path):
    return "{}{}".format(SERVER, path)

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
