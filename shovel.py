import shovel
import subprocess

@shovel.task
def test():
    subprocess.call('tox', shell=True)

@shovel.task
def ci_test():
    subprocess.call('tox -- --tags ~@wip --tags ~@later', shell=True)

@shovel.task
def debug_test():
    subprocess.call('KVAUT_LOG=DEBUG TOX_TESTENV_PASSENV=\"KVAUT_LOG\" tox -- --tags ~@wip --tags ~@later --no-capture --no-capture-stderr --no-logcapture --logging-level=DEBUG', shell=True)

@shovel.task
def debug_wip():
    subprocess.call('KVAUT_LOG=DEBUG TOX_TESTENV_PASSENV=\"KVAUT_LOG\" tox -- --tags @wip --no-capture --no-logcapture --no-capture-stderr --logging-level=DEBUG', shell=True)

@shovel.task
def wip():
    subprocess.call('tox -- --tags @wip', shell=True)

@shovel.task
def upload():
    subprocess.call('python setup.py sdist upload -r pypi', shell=True)

@shovel.task
def upload_test():
    subprocess.call('python setup.py sdist upload -r pypitest', shell=True)
