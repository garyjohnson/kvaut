#!/usr/bin/env python
import os, sys
import logging
sys.path.append(os.path.abspath('.'))

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.stacklayout import StackLayout

import kvaut.server
import kvaut.automator.factory
from kvaut.automator.custom_automator import CustomAutomator


logger = logging.getLogger(__name__)


class MyCustomWidgetAutomator(CustomAutomator):

    def is_match(self, value=None, **custom_attributes):
        if 'status' not in custom_attributes:
            return False

        return value in self.values and custom_attributes['status'] == self._target.status

    def get_children(self):
        return []

    def get_kv_ids(self):
        return []


class MyCustomWidget(Widget):
    status = StringProperty('')


class MyApp(App):
    def build(self):
        root = StackLayout()
        custom_widget1 = MyCustomWidget(id='my_custom_widget')
        custom_widget1.status = 'ok'
        custom_widget2 = MyCustomWidget(id='my_custom_widget')
        custom_widget2.status = 'nope'
        root.add_widget(custom_widget1)
        root.add_widget(custom_widget2)
        return root


kvaut.server.start_automation_server()
kvaut.automator.factory.register((MyCustomWidget,MyCustomWidgetAutomator))
MyApp().run()
