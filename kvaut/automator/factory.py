from __future__ import unicode_literals
import importlib
import logging


logger = logging.getLogger(__name__)

def automate(target):
    automators = ['Label','Widget']

    for class_name in automators:
        try:
            kivy_module = importlib.import_module('kivy.uix.{}'.format(class_name.lower()))
            kivy_type = getattr(kivy_module, class_name)

            automator_module = importlib.import_module('kvaut.automator.{}'.format(class_name.lower()))
            automator_type = getattr(automator_module, '{}Automator'.format(class_name))

            if kivy_type is not None and automator_type is not None and isinstance(target, kivy_type):
                return automator_type(target)
        except Exception as ex:
            logger.error('could not import {}: {}'.format(class_name, ex))
            continue

    raise Exception('No automator found for {}'.format(target))

