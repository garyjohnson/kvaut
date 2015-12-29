import collections
import logging

import kivy.app
from kivy.clock import Clock
import kvaut.automator.factory as factory
import kvaut.automator.tapper as tapper


logger = logging.getLogger(__name__)

class WidgetAutomator(object):

    def __init__(self, target, kv_id = None):
        self._kv_id = kv_id
        self._target = target

    def global_center(self):
        return self._target.to_window(self._target.center_x, self._target.center_y)

    @property
    def values(self):
        return [v for v in [self._target.id, self._kv_id] if v != None]

    def is_match(self, value=None, **custom_attributes):
        if any(custom_attributes):
            return False

        if value in self.values:
            return True

        return False

    def get_children(self):
        return [factory.automate(c) for c in self._target.children]

    def get_kv_ids(self):
        return [factory.automate(c, kv_id) for kv_id, c in self._target.ids.items()]

    def tap(self):
        tapper.tap(self)

    def to_json(self, is_recursive=False):
        x,y = self.global_center()

        json=collections.OrderedDict([ 
            ('type', self._target.__class__.__name__), 
            ('values', self.values),  
            ('global_position', {'x': x, 'y': y}),
        ])

        if is_recursive:
            children_json = []
            for child in self.get_children():
                children_json.append(child.to_json(is_recursive))
            json['children'] = children_json

        kv_ids = []
        for kv_id in self.get_kv_ids():
            kv_ids.append(kv_id.to_json(is_recursive))
        json['kv_ids'] = kv_ids

        return json

