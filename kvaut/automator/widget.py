import collections

import kvaut.automator.factory as factory


class WidgetAutomator(object):

    def __init__(self, target):
        self._target = target

    @property
    def values(self):
        return [self._target.id]

    def is_match(self, value=None):
        if value in self.values:
            return True

        return False

    def get_children(self):
        return [factory.automate(c) for c in self._target.children];

    def to_json(self, is_recursive=False):
        json=collections.OrderedDict([ 
            ('type',self._target.__class__.__name__), 
            ('values',self.values),  
        ])

        if is_recursive:
            children_json = []
            for child in self.get_children():
                children_json.append(child.to_json(is_recursive))
            json['children'] = children_json

        return json

