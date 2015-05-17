#!/usr/bin/env python
import os, sys
import kivy
from kivy.app import App
from kivy.uix.widget import Widget


class MyApp(App):

    def build(self):
        return Widget(id='my_widget')

MyApp().run()
