import sys
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

setup(
    name='kvaut',
    version='0.0.5',
    author='Gary Johnson',
    author_email = 'gary@gjtt.com',
    description = 'Automation for BDD testing Kivy apps',
    install_requires=['bottle'],
    tests_require=['bottle'],
    license = 'MIT License',
    packages = ['kvaut', 'kvaut.automator', 'kvaut.errors', 'kvaut.helpers'],
    )
