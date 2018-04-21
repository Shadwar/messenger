from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import NumericProperty
from kivy.uix.label import Label


class Message(Label):
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)

    def __init__(self, **kwargs):
        is_user = kwargs['is_user']
        del kwargs['is_user']
        if is_user:
            self.r = 0
            self.g = 1
            self.b = 1
        else:
            self.r = 1
            self.g = 1
            self.b = 0

        super().__init__(**kwargs)
