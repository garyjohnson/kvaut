#!/usr/bin/env python
import os, sys
sys.path.append(os.path.abspath('.'))
import kvaut.server as kvaut

kvaut.start_automation_server_if_in(sys.argv)

import kivy
import kivy.app
import kivy.uix

class MyApp(kivy.app.App):

    def build(self):
        return kivy.uix.widget.Widget(id='my_widget')

MyApp().run()


