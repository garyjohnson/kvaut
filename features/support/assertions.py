from nose.tools import *

def assert_raises(callable, error_type, message):
    raised_error = False
    try:
        callable()
    except error_type as ex:
        raised_error = True

    assert_true(raised_error, message)
