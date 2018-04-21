import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label


class P(App):
    def build(self):
        l = Button(text='', size_hint=(None, None), size=(300, 100))
        a = Label(text='asdf', halign='left', x=50)
        img = Image(source='no_user_avatar.png')
        l.add_widget(img)
        l.add_widget(a)

        print(dir(l))
        print(l.children)
        return l

P().run()