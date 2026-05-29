"""Test app: a widget with opacity 0 to test visibility rules."""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class HiddenApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        visible = Button(text='Visible')
        visible.id = 'visible'
        hidden = Button(text='Hidden', opacity=0)
        hidden.id = 'hidden'
        root.add_widget(visible)
        root.add_widget(hidden)
        return root


if __name__ == '__main__':
    HiddenApp().run()
