from kivy import Config

from kivy_client.client_app import ClientApp

if __name__ == '__main__':
    Config.set('graphics', 'width', 1024)
    Config.set('graphics', 'height', 800)
    Config.write()

    ClientApp().run()
