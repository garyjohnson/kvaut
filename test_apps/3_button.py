#!/usr/bin/env python
import os, sys
sys.path.append(os.path.abspath('.'))
import kvaut.server as kvaut

import kivy
from kivy.app import App
from kivy.uix.button import Button


class MyApp(App):

    def build(self):
        return Button(text='Hello world')

kvaut.start_automation_server()
MyApp().run()
