import logging

from behave import use_step_matcher

import features.support.app_helpers as app_helpers


use_step_matcher("re")
logging.getLogger("requests").setLevel(logging.ERROR)

def before_all(context):
    context.config.setup_logging()

def after_scenario(context, scenario):
    app_helpers.kill_app(context)
