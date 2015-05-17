class WidgetAutomator(object):

    def __init__(self, target):
        self._target = target

    @property
    def values(self):
        return [self._target.id]

    @property
    def automation_types(self):
        return [c.__name__ for c in self._target.__bases__]

    def is_match(self, value=None, automation_type=None):
        if automation_type and automation_type not in self.automation_types:
            return False

        if value in self.values:
            return True

        return False

    def get_children(self):
        return [factory.automate(c) for c in self._target.children];

    def to_json(self, is_recursive=False):
        json=OrderedDict([ 
            ('type',self._target.__class__.__name__), 
            ('values',self.get_values()),  
        ])

        if is_recursive:
            children_json = []
            for child in self.get_children():
                children_json.append(child.to_json(is_recursive))
            json['children'] = children_json

        return json

