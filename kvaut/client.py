from __future__ import unicode_literals
import os
import time
import json
import logging

import requests
from nose.tools import assert_true 

from kvaut.helpers.wait import *
import kvaut.errors


JSON_HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json' }
SERVER="http://0.0.0.0:5155"
TIMEOUT=3

def assert_is_active(target):
    element = find_element(target)
    logger.debug("found element:")
    logger.debug(element)

def assert_is_not_active(target):
    element = find_element(target)
    logger.debug("found element:")
    logger.debug(element)

def assert_is_visible(target, **kwargs):
    if not wait_for(lambda: find_element(target, **kwargs)):
        raise kvaut.errors.AssertionError('Could not find element matching \"{}\"'.format(target))

def find_above(above, below):
    above_element = find_element(above)
    below_element = find_element(below)

    above_y = above_element.get('global_position', {}).get('y', 0)
    below_y = below_element.get('global_position', {}).get('y', 0)
    logger.debug('Found expected above element \'{}\' at Y position {}, below element \'{}\' at Y position {}'.format(above_element, above_y, below_element, below_y))
    return above_y > below_y

def find_leading(leading, trailing):
    leading_element = find_element(leading)
    trailing_element = find_element(trailing)

    leading_x = leading_element.get('global_position', {}).get('x', 0)
    trailing_x = trailing_element.get('global_position', {}).get('x', 0)
    logger.debug('Found expected leading element \'{}\' at X position {}, trailing element \'{}\' at X position {}'.format(leading_element, leading_x, trailing_element, trailing_x))
    return leading_x < trailing_x

def assert_is_above(above, below):
    assert_is_visible(above)
    assert_is_visible(below)

    if not wait_for(lambda: find_above(above, below)):
        raise kvaut.errors.AssertionError('Expected {} to be above {}'.format(above, below))

def assert_is_leading(leading, trailing):
    assert_is_visible(leading)
    assert_is_visible(trailing)

    if not wait_for(lambda: find_leading(leading, trailing)):
        raise kvaut.errors.AssertionError('Expected {} to be leading {}'.format(leading, trailing))

def find_element(target, **kwargs):
    found_element = None

    if kwargs is None:
        kwargs = {}

    try:
        body = {'query':{'value':target, 'custom_attributes':kwargs}}
        response = requests.post(url_for('/find_element'), data=json.dumps(body), headers=JSON_HEADERS, timeout=TIMEOUT)
        found_element = response.json()
        if len(found_element.keys()) == 0:
            found_element = None
    except Exception as ex:
        logger.debug('error occurred attempting to find element matching \"{}\": {}'.format(target, ex))

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

    logger.debug("tapped element {}".format(tapped_element))
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
