"""Test app: a TextInput and label."""

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class InputApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        self.input = TextInput(text='')
        self.input.id = 'name_input'
        self.label = Label(text='Hello!')
        self.label.id = 'greeting'
        root.add_widget(self.input)
        root.add_widget(self.label)
        return root


if __name__ == '__main__':
    InputApp().run()
