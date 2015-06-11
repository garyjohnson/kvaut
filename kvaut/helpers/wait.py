import time


def wait_for(condition, retries=6, loop_delay=0.5):
    met_condition = False
    for i in range(0, retries):
        time.sleep(loop_delay)
        met_condition = condition()
        if met_condition:
            break

    return met_condition
