from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class MyApp(App):
    def build(self):
        layout = FloatLayout()
        label = Label(
            text='test',
            pos=(20, 20),
            size=(180, 100),
            size_hint=(None, None))
        with label.canvas:
            Color(0, 1, 1, 0.25)
            Rectangle(pos=label.pos, size=label.size)

        layout.add_widget(label)

        return layout


if __name__ == '__main__':
    MyApp().run()