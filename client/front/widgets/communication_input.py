from kivy.properties import ObjectProperty, Clock
from kivy.uix.widget import Widget

from client.client import Client
from client.front.widgets.smile import Smile

smiles_dict = {
    ':)': u'😀',
    ':D': u'😃',
    ';)': u'😉',
    ':P': u'😋',
    ':(': u'😞'
}


class CommunicationInput(Widget):
    input_field = ObjectProperty(None)
    submit_button = ObjectProperty(None)
    smile_container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = Client()
        Clock.schedule_once(self.init_smiles, 0)
        Clock.schedule_once(self.init_submit, 0)

    def init_smiles(self, dt):
        for text, code in smiles_dict.items():
            smile = Smile(text=code)
            smile.on_release = self.smile_clicked(code)
            self.ids.smile_container.add_widget(smile)

    def init_submit(self, dt):
        def inner():
            text = self.ids.input_field.text
            self.ids.input_field.text = ''
            self.client.send_event({'action': 'ui_send_message_clicked', 'message': text})

        self.ids.submit_button.on_press = inner

    def smile_clicked(self, smile):
        def inner():
            self.ids.input_field.text += smile
        return inner
