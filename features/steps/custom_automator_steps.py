from behave import *
from nose.tools import *
from features.support.assertions import *

import kvaut.client


@step(u'I see "(?P<target>[^"]*)" with custom criteria')
def i_see_with_custom_criteria(context, target):
    kvaut.client.assert_is_visible(target, test='test')
