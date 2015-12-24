from functools import partial
import logging

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.base import EventLoop

from kvaut.automator.fake_motion_event import FakeMotionEvent


logger = logging.getLogger(__name__)

def tap(automator):
    Clock.schedule_once(partial(_tap_on_ui_thread, automator), 0)

@mainthread
def _tap_on_ui_thread(automator, args):
    global_x,global_y = automator.global_center()
    app = App.get_running_app()
    
    relative_pos = {"x": global_x * 2 / app.root.width, "y" : global_y * 2 / app.root.height}
    touch = FakeMotionEvent("fake", 1, relative_pos)
     
    EventLoop.post_dispatch_input("begin", touch)
    EventLoop.post_dispatch_input("end", touch)
