import kvaut.client


@then(u'I see "(?P<target>[^"]*)" is not active')
def i_see_is_not_active(context, target):
    kvaut.client.assert_is_active(target)

@then(u'I see "(?P<target>[^"]*)" is active')
def i_see_is_active(context, target):
    kvaut.client.assert_is_not_active(target)
