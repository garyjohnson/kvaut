#!/usr/bin/env python
import os, sys
sys.path.append(os.path.abspath('.'))
import kvaut.server as kvaut

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty


class MyCustomWidget(Widget):
    is_active = BooleanProperty(False)


class MyApp(App):

    def build(self):
        custom_widget = MyCustomWidget(id='my_custom_widget')
        custom_widget.is_active = True
        return custom_widget


kvaut.start_automation_server()
MyApp().run()
