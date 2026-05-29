"""Test app: a screen with a kv lang id to test by_id selectors."""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class IdApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        label = Label(text='Label Text')
        label.id = 'my_label'
        root.add_widget(label)
        return root


if __name__ == '__main__':
    IdApp().run()
