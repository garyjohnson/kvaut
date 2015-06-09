import os
import subprocess


LOG_DEBUG = 10

def launch_app(context, app_name):
    kwargs = {'env':os.environ}
    context.dev_null = open(os.devnull, 'w')
    if context.config.logging_level > LOG_DEBUG:
        kwargs.update({'stdout':context.dev_null, 'stderr':context.dev_null})

    context.test_app_process = subprocess.Popen(["python", "test_apps/{0}".format(app_name)], **kwargs)

def kill_app(context):
    if context.test_app_process:
        subprocess.Popen.kill(context.test_app_process)
