from __future__ import print_function

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior

from kivy.graphics import *

from kivy.app import App

import pprint

import utils

class FileView(ToggleButtonBehavior, BoxLayout):
    f = ObjectProperty(None)
    def __init__(self, group, f, selected, **kwargs):
        super(FileView, self).__init__(**kwargs)
        self.group = group
        self.f = f
        #self.bind(state=self.on_state)
        self.selected = selected

    def on_state(self, button, state):
        if state == 'normal':
            self.setBackground(0.4, 0.4, 0.4)
        elif state == 'down':
            self.setBackground(0.6, 0.6, 0.6)

    def setBackground(self, r, g, b):
        with self.canvas.before:
            Color(r, g, b, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.5, 0.5, 0.5, 1)
            Line(points=[self.pos[0]+15, self.pos[1], self.pos[0]+self.width-15, self.pos[1]])

class FileList(GridLayout):
    files = ListProperty(None)
    selected = ObjectProperty({})

    def on_files(self, inst, files):
        self.cols = 1
        self.size_hint_y = None
        self.padding = (0, 0)
        self.spacing = (0, 0)
        self.bind(minimum_height=self.setter('height'))

        self.clear_widgets()

        for i in range(len(files)):
            minfile = None
            for f in files:
                if minfile == None or f['date'] < minfile['date']:
                    minfile = f

            if minfile != None:
                files.remove(minfile)
                btn = FileView('files', minfile, self.selected, size_hint_y=None, height=60)
                btn.bind(state=self.update_selected)
                self.add_widget(btn)

    def update_selected(self, inst, value):
        f = inst.f

        if value == 'down':
            self.selected = f
        else:
            for i in ToggleButtonBehavior.get_widgets('files'):
                if i.state == 'down':
                    return

            self.selected = {}


class SystemCommands(GridLayout):
    commands = ObjectProperty(None)

    def on_commands(self, inst, newcommands):

        self.orientation = 'vertical'
        self.cols = 1

        self.clear_widgets()

        if newcommands == None:
            return

        for source in newcommands:
            commands = newcommands[source]

            commandbox = GridLayout(rows = 1)
            commandbox.size_hint_y = None
            commandbox.height = 50

            for command in commands:

                if command['action'] == 'divider':
                    self.add_widget(commandbox)
                    commandbox = GridLayout(rows = 1)
                    commandbox.size_hint_y = None
                    commandbox.height = 50
                else:
                    btn = Button()
                    btn.text = command['name']

                    if 'confirm' in command and (command['confirm'] != "" or command['confirm'] != None):
                        btn.background_color = (2, .5, .5, 1)

                    btn.on_press = lambda source=command['source'], action=command['action']: App.get_running_app().client.sendCommand('api/system/commands/' + str(source) + '/' + str(action) , '')
                    commandbox.add_widget(btn)

            self.add_widget(commandbox)

class TempKeypad(BoxLayout):

    tempBox = ObjectProperty(None)

    profile = None
    oldProfile = None

    tempIn = ObjectProperty(None)
    tool = ""

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]) and not self.ids.keypad.collide_point(touch.pos[0], touch.pos[1]):
            return True
        else:
            if not self.collide_point(touch.pos[0], touch.pos[1]):
                self.remove()
                return False
            elif super(TempKeypad, self).on_touch_down(touch):
                return True
            else:
                return False

    def remove(self):
        if self.tempIn.text != "":
            if self.tool == 'bed':
                App.get_running_app().client.sendCommand('/api/printer/bed', 'target', {'target': int(self.tempIn.text)})
            else:
                App.get_running_app().client.sendCommand('/api/printer/tool', 'target', {'targets': {self.tool: int(self.tempIn.text)}})
        self.parent.remove_widget(self)

class TemperatureLabel(BoxLayout):
    title = StringProperty("")
    name = StringProperty("")
    actual = StringProperty("")
    target = StringProperty("")

class TemperatureBox(BoxLayout):
    bed = BooleanProperty(False)
    tools = NumericProperty(0)
    buttons = BooleanProperty(False)

    def make_labels(self):

        App.get_running_app().client.bind(temps=self.updateTemps)
        if self.bed:
            bed_widget = TemperatureLabel()
            bed_widget.title = "Bed:"
            bed_widget.name = 'bed'

            if self.buttons:
                setbtn = Button()
                setbtn.text = "Set"
                setbtn.size_hint_x = 0.3
                setbtn.on_press = lambda: self.showKeyboard('bed', "Bed")
                bed_widget.add_widget(setbtn)

            self.add_widget(bed_widget)

        if self.tools == 1:
            extuder_widget = TemperatureLabel()
            extuder_widget.title = "Tool:"
            extuder_widget.name = 'tool0'

            if self.buttons:
                setbtn = Button()
                setbtn.text = "Set"
                setbtn.size_hint_x = 0.3
                setbtn.on_press = lambda: self.showKeyboard('tool0', "Tool")
                extuder_widget.add_widget(setbtn)

            self.add_widget(extuder_widget)
        else:
            for i in range(self.tools):
                extuder_widget = TemperatureLabel()
                extuder_widget.title = "Tool " + str(i) + ":"
                extuder_widget.name = 'tool' + str(i)

                if self.buttons:
                    setbtn = Button()
                    setbtn.text = "Set"
                    setbtn.size_hint_x = 0.15
                    setbtn.size_hint_y = 1
                    setbtn.on_press = lambda i=i: self.showKeyboard('tool' + str(i), "Tool " + str(i) + ":")
                    extuder_widget.add_widget(setbtn)

                    selbtn = Button()
                    selbtn.text = "Sel"
                    selbtn.size_hint_x = 0.15
                    setbtn.size_hint_y = 1
                    selbtn.on_press = lambda i=i: App.get_running_app().client.sendCommand('api/printer/tool', 'select', {'tool': 'tool' + str(i)})
                    extuder_widget.add_widget(selbtn);

                self.add_widget(extuder_widget)

    def on_bed(self, inst, newbed):
        self.clear_widgets()
        self.make_labels()

    def on_tools(self, inst, newtools):
        self.clear_widgets()
        self.make_labels()

    def updateTemps(self, inst, newtemps):
        for i in self.children:
            if isinstance(i, TemperatureLabel):
                target = utils.get(newtemps, [i.name, 'target'], 0)
                if target < 2:
                    i.target = ''
                else:
                    i.target = str(round(target, 1))

                actual = utils.get(newtemps, [i.name, 'actual'], 0)
                if actual < 2:
                    i.actual = ''
                else:
                    i.actual = str(round(actual, 1))
            else:
                for j in i.children:
                    if isinstance(j, TemperatureLabel):
                        target = utils.get(newtemps, [j.name, 'target'], 0)
                        if target < 2:
                            j.target = ''
                        else:
                            j.target = str(round(target, 1))

                        actual = utils.get(newtemps, [j.name, 'actual'], 0)
                        if actual < 2:
                            j.actual = ''
                        else:
                            j.actual = str(round(actual, 1))

    def showKeyboard(self, tool, title):
        keypad = TempKeypad()
        keypad.title = title
        keypad.tool = tool

        self.get_root_window().children[0].add_widget(keypad)

class FilamentLabel(BoxLayout):
    title = StringProperty("")
    name = StringProperty("")
    length = StringProperty("")
    volume = StringProperty("")

class FilamentBox(BoxLayout):
    tools = NumericProperty(0)

    def make_labels(self):
        App.get_running_app().client.bind(job=self.updateFilament)
        if self.tools == 1:
            extuder_widget = FilamentLabel()
            extuder_widget.title = "Filament:"
            extuder_widget.name = 'tool0'
            self.add_widget(extuder_widget)
        else:
            for i in range(self.tools):
                extuder_widget = FilamentLabel()
                extuder_widget.title = "Tool " + str(i) + " Usage:"
                extuder_widget.name = 'tool' + str(i)
                self.add_widget(extuder_widget)

    def on_bed(self, inst, newbed):
        self.clear_widgets()
        self.make_labels()

    def on_tools(self, inst, newtools):
        self.clear_widgets()
        self.make_labels()

    def updateFilament(self, inst, newjob):
        for i in self.children:
            if isinstance(i, FilamentLabel):
                length = utils.get(newjob, ['filament', i.name, 'length'], 0)
                if length < 2:
                    i.length = ''
                else:
                    i.length = str(round(length/1000, 2))

                volume = utils.get(newjob, ['filament', i.name, 'volume'], 0)
                if volume < 2:
                    i.volume = ''
                else:
                    i.volume = str(round(volume, 2))
