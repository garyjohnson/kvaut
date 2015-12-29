import kvaut.client


@step(u'"(?P<above>[^"]*)" is above "(?P<below>[^"]*)"')
def is_above(context, above, below):
    kvaut.client.assert_is_above(above, below)

@step(u'"(?P<leading>[^"]*)" is leading "(?P<trailing>[^"]*)"')
def is_leading(context, leading, trailing):
    kvaut.client.assert_is_leading(leading, trailing)
