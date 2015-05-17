from behave import *
from nose.tools import *
from features.support.assertions import *

import kvaut.client
import kvaut.errors
import features.support.app_helpers as app_helpers

@when('I launch "(?P<app_name>[^"]*)"')
def i_launch(context, app_name):
    app_helpers.launch_app(context, app_name)

@given('I am running "(?P<app_name>[^"]*)"')
def i_am_running_app(context, app_name):
    app_helpers.launch_app(context, app_name)
    kvaut.client.wait_for_automation_server()

@then('I see "(?P<target>[^"]*)"')
def then_i_see(context, target):
    kvaut.client.assert_is_visible(target)

@then('I do not see "(?P<target>[^"]*)"')
def then_i_do_not_see(context, target):
    assert_raises(lambda: kvaut.client.assert_is_visible(target), kvaut.errors.AssertionError, "Expected error to occur when asserting visible")

@then(u'I get an error waiting for automation server')
def i_get_an_error_waiting_for_automation_server(context):
    assert_raises(lambda: kvaut.client.wait_for_automation_server(), kvaut.errors.ServerNotFoundError, "Expected error to occur when waiting for automation server")


