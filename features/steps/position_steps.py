import kvaut.client


@step(u'"(?P<above>[^"]*)" is above "(?P<below>[^"]*)"')
def is_above(context, above, below):
    kvaut.client.assert_is_above(above, below)
