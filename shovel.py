import shovel
import subprocess

@shovel.task
def wip():
    subprocess.call('behave --tags @wip', shell=True)
