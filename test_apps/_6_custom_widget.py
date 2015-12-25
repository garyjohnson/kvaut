#!/usr/bin/env python
import os, sys
import logging
sys.path.append(os.path.abspath('.'))
import kvaut.server
import kvaut.automator.factory
from kvaut.automator.custom_automator import CustomAutomator

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty


logger = logging.getLogger(__name__)

class MyCustomWidgetAutomator(CustomAutomator):

    def is_match(self, value=None, **custom_attributes):
        super_matches = super(MyCustomWidgetAutomator, self).is_match(value, **custom_attributes)

        if 'is_active' not in custom_attributes:
            return False

        attr_matches = custom_attributes.get('is_active').lower() == str(self._target.is_active).lower()
        return super_matches and attr_matches


class MyCustomWidget(Widget):
    is_active = BooleanProperty(False)

class MyApp(App):
    def build(self):
        custom_widget = MyCustomWidget(id='my_custom_widget')
        custom_widget.is_active = True
        return custom_widget


kvaut.server.start_automation_server()
kvaut.automator.factory.register((MyCustomWidget,MyCustomWidgetAutomator))
MyApp().run()
