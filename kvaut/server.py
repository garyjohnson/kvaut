from __future__ import unicode_literals
import os
import threading
import logging

import bottle

import kvaut.automator.factory as factory


@bottle.get("/ping")
def ping():
    if get_root_widget() is None:
        bottle.abort(503, "Still booting up, try again later")

    return 'Ping!'

@bottle.get("/tree")
def tree():
    widget = get_root_widget()
    if widget is not None:
        return widget.to_json(is_recursive=True)

@bottle.post("/find_element")
def find_element():
    found_json = {}
    value = get_query_value('value')
    custom_attributes = get_query_value('custom_attributes', default={})

    widget = find_widget_in(get_root_widget(), value=value, **custom_attributes)
    if widget is not None:
        found_json = widget.to_json()

    logger.debug('found element: {}'.format(found_json))
    return found_json

@bottle.post("/tap")
def tap():
    found_json = {}
    value = get_query_value('value')
    custom_attributes = get_query_value('custom_attributes', default={})

    widget = find_widget_in(get_root_widget(), value=value, **custom_attributes)
    if widget is not None:
        found_json = widget.to_json()
        widget.tap()

    return found_json

def get_query_value(name, default=''):
    if bottle.request.json is not None:
        return bottle.request.json.get('query', {}).get(name, default)

    return default

def get_root_widget():
    import kivy.app
    app = kivy.app.App.get_running_app()
    return factory.automate(app.root)

def find_widget_in(parent, value=None, **custom_attributes):
    if parent is None:
        return None

    if parent.is_match(value=value, **custom_attributes):
        return parent

    for kv_id in parent.get_kv_ids():
        if kv_id.is_match(value=value, **custom_attributes):
            return kv_id

    for child in parent.get_children():
        if child.is_match(value=value, **custom_attributes):
            return child

        found_widget = find_widget_in(child, value=value, **custom_attributes)
        if found_widget is not None:
            return found_widget

    return None

def start_automation_server():
    if os.environ.get('KVAUT_ENABLE', None):
        logger.info('kvaut server starting...')
        debug = log_level_name is 'DEBUG'
        thread = threading.Thread(target=bottle.run, kwargs={'host':'0.0.0.0', 'port':5155, 'quiet':(not debug), 'debug':debug})
        thread.setDaemon(True)
        thread.start()
    else:
        logger.info('kvaut is disabled!')


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
