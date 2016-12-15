import os
os.environ["KIVY_NO_ARGS"] = "1"
#os.environ["KIVY_NO_CONSOLELOG"] = "1"

PATH_BASE = os.path.join(os.getcwd(), os.path.dirname(__file__))

#print os.getcwd()
#print __file__
#print("PATH_BASE: ")
#print(PATH_BASE)
#print(os.path.join(PATH_BASE, 'data/fonts/Ubuntu-R.ttf'))

import kivy
kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger
from kivy.uix.settings import Settings
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.text import LabelBase
from kivy.config import Config
from kivy.garden import iconfonts

import thread

from widgets import *

from client import Client

Config.set('graphics', 'height', '480')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'borderless', '0')
Config.write()

VKeyboard.key_background_color = [0.2, 0.2, 0.2, 1]
VKeyboard.margin_hint = [0, 0, 0, 0]

LabelBase.register(name="Ubuntu",
                   fn_regular    = os.path.join(PATH_BASE, 'data/fonts/Ubuntu-R.ttf'),
                   fn_bold       = os.path.join(PATH_BASE, 'data/fonts/Ubuntu-B.ttf'),
                   fn_italic     = os.path.join(PATH_BASE, 'data/fonts/Ubuntu-RI.ttf'),
                   fn_bolditalic = os.path.join(PATH_BASE, 'data/fonts/Ubuntu-BI.ttf'))

iconfonts.register('default_font', os.path.join(PATH_BASE, 'data/fonts/font-awesome.ttf'), os.path.join(PATH_BASE, 'data/fonts/font-awesome.fontd'))

settingsjson = '''
[
    {
        "type": "string",
        "title": "Octoprint Address",
        "desc": "The IP to use for connecting to Octoprint",
        "section": "Octoscreen",
        "key": "host"
    },
    {
        "type": "numeric",
        "title": "Octoprint Port",
        "desc": "The port to use for connecting to Octoprint",
        "section": "Octoscreen",
        "key": "port"
    },
    {
        "type": "string",
        "title": "Octoprint API Key",
        "desc": "The API Key to use for connecting to Octoprint",
        "section": "Octoscreen",
        "key": "apikey"
    }
]
'''

settingsdefaults = {
    'host': '127.0.0.1',
    'port': 5000,
    'apikey': ''
}

class OctoprintLcd(FloatLayout):

    def switchDefault(self):
        self.ids.tabbedpanel.switch_to(self.ids.tabbedpanel.default_tab)

class OctoprintLcdApp(App):

    client = ObjectProperty(None)

    def __init__(self):
        super(OctoprintLcdApp, self).__init__()


    def build(self):

        self.settings_cls = Settings

        self.client = Client()
        self.client.init(self.config.get('Octoscreen', 'host'), self.config.get('Octoscreen', 'port'), self.config.get('Octoscreen', 'apikey'))
        return OctoprintLcd()

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('Octoscreen', settingsdefaults)

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        settings.add_json_panel('Octoscreen', self.config, data=settingsjson)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

    def close_settings(self, settings):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        self.client.init(self.config.get('Octoscreen', 'host'), self.config.get('Octoscreen', 'port'), self.config.get('Octoscreen', 'apikey'))
        super(OctoprintLcdApp, self).close_settings(settings)

OctoprintLcdApp.run(OctoprintLcdApp())
