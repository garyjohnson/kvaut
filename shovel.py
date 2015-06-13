import shovel
import subprocess

@shovel.task
def test():
    subprocess.call('KVAUT_LOG=DEBUG behave --tags ~@wip --tags ~@later --no-capture --no-logcapture --logging-level DEBUG', shell=True)

@shovel.task
def wip():
    subprocess.call('behave --tags @wip', shell=True)
