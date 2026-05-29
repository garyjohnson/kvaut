"""Test app: multiple widgets with same text to test ambiguous matching."""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class AmbiguousApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        btn1 = Button(text='Duplicate')
        btn1.id = 'btn1'
        btn2 = Button(text='Duplicate')
        btn2.id = 'btn2'
        root.add_widget(btn1)
        root.add_widget(btn2)
        return root


if __name__ == '__main__':
    AmbiguousApp().run()
