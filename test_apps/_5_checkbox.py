#!/usr/bin/env python
import os, sys
sys.path.append(os.path.abspath('.'))
import kvaut.server as kvaut

import kivy
from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Rectangle


class _5_CheckBoxApp(App):
    pass

kvaut.start_automation_server()
_5_CheckBoxApp().run()
