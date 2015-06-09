import shovel
import subprocess

@shovel.task
def test():
    subprocess.call('behave --tags ~@wip --tags ~@later', shell=True)

@shovel.task
def wip():
    subprocess.call('behave --tags @wip', shell=True)
