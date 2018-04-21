from kivy.properties import ObjectProperty, Clock
from kivy.uix.button import Button


class Contact(Button):
    """ Контакт пользователя """
    image_avatar = ObjectProperty(None)

    def __init__(self, avatar='no_user_avatar.png', **kwargs):
        self.avatar = avatar
        kwargs['text'] = kwargs['text'].ljust(18)
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, dt):
        self.ids.image_avatar.source = self.avatar
