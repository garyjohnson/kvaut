import shovel
import subprocess

@shovel.task
def test():
    subprocess.call('tox', shell=True)

@shovel.task
def ci_test():
    subprocess.call('behave --tags ~@wip --tags ~@later', shell=True)

@shovel.task
def debug_test():
    subprocess.call('KVAUT_LOG=DEBUG behave --tags ~@wip --tags ~@later --no-capture --no-logcapture --logging-level DEBUG', shell=True)

@shovel.task
def wip():
    subprocess.call('behave --tags @wip', shell=True)

@shovel.task
def upload():
    subprocess.call('python setup.py sdist upload -r pypi', shell=True)

@shovel.task
def upload_test():
    subprocess.call('python setup.py sdist upload -r pypitest', shell=True)
