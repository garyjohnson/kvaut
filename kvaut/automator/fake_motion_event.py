from kivy.input.motionevent import MotionEvent

class FakeMotionEvent(MotionEvent):
 
    def depack(self, args):
        self.is_touch = True
        self.sx = args['x']
        self.sy = args['y']
        self.profile = ['pos']
        super(FakeMotionEvent, self).depack(args)
