"""Test app: a simple button that changes text when tapped."""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout


class ButtonApp(App):
    def build(self):
        root = StackLayout()
        btn = Button(text='Hello world', size=(100, 25), size_hint=(None, None))
        btn.bind(on_press=lambda instance: setattr(btn, 'text', 'Howdy'))
        root.add_widget(btn)
        return root


if __name__ == '__main__':
    ButtonApp().run()
