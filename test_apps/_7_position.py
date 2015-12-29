#!/usr/bin/env python
import os, sys
import logging
sys.path.append(os.path.abspath('.'))

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics import Color

import kvaut.server


class MyApp(App):
    def build(self):
        root = FloatLayout(size=(600,600), pos=(0,0))
        with root.canvas:
            Color(1,1,0)
            Rectangle(pos=root.pos, size=root.size)

        widget1 = Widget(id='top', size=(50,50), pos=(0,0))
        with widget1.canvas:
            Color(1,0,1)
            Rectangle(pos=widget1.pos, size=widget1.size)

        widget2 = Widget(id='bottom', size=(50,50), pos=(0,100))
        with widget2.canvas:
            Color(0,1,1)
            Rectangle(pos=widget2.pos, size=widget2.size)

        root.add_widget(widget1)
        root.add_widget(widget2)
        return root


kvaut.server.start_automation_server()
MyApp().run()
