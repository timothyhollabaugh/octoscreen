import os
os.environ["KIVY_NO_ARGS"] = "1"
#os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy
kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

from kivy.config import Config

import thread

from widgets import *

from client import Client

Config.set('graphics', 'height', '480')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'borderless', '0')
Config.write()

class OctoprintLcd(FloatLayout):

    def switchDefault(self):
        self.ids.tabbedpanel.switch_to(self.ids.tabbedpanel.default_tab)

class OctoprintLcdApp(App):

    client = ObjectProperty(None)

    def __init__(self):
        super(OctoprintLcdApp, self).__init__()

        self.client = Client()

        Clock.schedule_once(self.client.init)


    def build(self):
        return OctoprintLcd()

OctoprintLcdApp.run(OctoprintLcdApp())
