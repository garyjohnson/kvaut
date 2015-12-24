from behave import *
from nose.tools import *
from features.support.assertions import *

import kvaut.client


@step(u'I see "(?P<target>[^"]*)" with attributes')
def i_see_with_attributes(context, target):
    attributes = {}
    for row in context.table:
        attributes[row['name']] = row['value']

    kvaut.client.assert_is_visible(target, **attributes)

@step(u'I do not see "(?P<target>[^"]*)" with attributes')
def i_do_not_see_with_attributes(context, target):
    attributes = {}
    for row in context.table:
        attributes[row['name']] = row['value']

    assert_raises(lambda: kvaut.client.assert_is_visible(target, **attributes), kvaut.errors.AssertionError, "Expected error to occur when asserting visible")
