from kivy.properties import ObjectProperty, Clock
from kivy.uix.button import Button
from client.assets.assets import assets


class UserInfo(Button):
    """ Информация о самом пользователе """
    image_avatar = ObjectProperty(None)

    def __init__(self, avatar=assets['no_user_avatar'], **kwargs):
        self.avatar = avatar
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, dt):
        self.ids.image_avatar.source = self.avatar
