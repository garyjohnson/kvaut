import collections

import kvaut.automator.factory as factory
import kvaut.automator.widget


class LabelAutomator(kvaut.automator.widget.WidgetAutomator):

    def __init__(self, target):
        self._target = target

    @property
    def values(self):
        return [self._target.text, self._target.id]

