from kivy.properties import ObjectProperty, Clock
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from .smile import Smile


class CommunicationInput(Widget):
    input_field = ObjectProperty(None)
    submit_button = ObjectProperty(None)
    smile_container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_smiles, 0)

    def init_smiles(self, dt):
        for i in range(5):
            smile = Smile(text='')
            self.ids.smile_container.add_widget(smile)
