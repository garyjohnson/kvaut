import time


def wait_for(condition, retries=6, loop_delay=0.5):
    met_condition = False
    retry_count = 0
    while (retry_count < retries and not met_condition):
        retry_count += 1
        time.sleep(loop_delay)
        met_condition = condition()

    return met_condition
