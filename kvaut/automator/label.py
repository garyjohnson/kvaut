import collections

import kvaut.automator.factory as factory
import kvaut.automator.widget


class LabelAutomator(kvaut.automator.widget.WidgetAutomator):

    @property
    def values(self):
        return [self._target.text, self._target.id]

