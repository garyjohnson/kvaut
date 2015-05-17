#!/usr/bin/env python
import os, sys
sys.path.append(os.path.abspath('.'))
import kvaut.server as kvaut

import kivy
from kivy.app import App
from kivy.uix.widget import Widget


class MyApp(App):

    def build(self):
        return Widget(id='my_widget')

kvaut.start_automation_server()
MyApp().run()


