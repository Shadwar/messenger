from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


class Contact(Button):
    login = ObjectProperty(None)
    image_avatar = ObjectProperty(None)

    def __init__(self, avatar='no_user_avatar.png', **kwargs):
        self.avatar = avatar
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, dt):
        self.ids.image_avatar.source = self.avatar


class ContactList(ScrollView):
    container = ObjectProperty(None)

    def add_item(self, item):
        contact = Contact(text=item)
        self.ids.container.add_widget(contact)


class Test(Widget):
    contact_list = ObjectProperty(None)

    def update(self, dt):
        pass


class ClientApp(App):
    def build(self):
        cl = Test()
        print(dir(cl.ids.contact_list))
        for i in range(3):
            cl.ids.contact_list.add_item('button-{}'.format(i))

        Clock.schedule_interval(cl.update, 1.0 / 10.0)
        return cl


if __name__ == '__main__':
    Builder.load_file('new_kivy_client.kv')
    Config.set('graphics', 'width', 1024)
    Config.set('graphics', 'height', 800)
    Config.write()

    ClientApp().run()
