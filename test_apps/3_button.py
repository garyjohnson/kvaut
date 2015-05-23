#!/usr/bin/env python
import os, sys
sys.path.append(os.path.abspath('.'))
import kvaut.server as kvaut

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout


class MyApp(App):

    def build(self):
        root = StackLayout()
        button1 = Button(text='Hello world', size=(100,25), size_hint=(None,None))
        button2 = Button(id='goodbye_world', text='test', size=(100,25), size_hint=(None,None))
        root.add_widget(button1)
        root.add_widget(button2)
        return root

kvaut.start_automation_server()
MyApp().run()
