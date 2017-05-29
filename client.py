from __future__ import print_function

from octoprint import init_settings
import octoprint_client

from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.logger import Logger

import pprint

import json 

class Client(EventDispatcher):

    socket = None
    octoprintClient = None

    octoprintConnection = StringProperty('Connecting')

    logs = ListProperty([])
    offsets = ListProperty([])
    busyFiles = ListProperty([])
    messages = ListProperty([])
    state = ObjectProperty(None, allownone=True)
    serverTime = NumericProperty(0)
    temps = ObjectProperty(None, allownone=True)
    temp = ObjectProperty(None, allownone=True)
    job = ObjectProperty(None, allownone=True)
    currentZ = NumericProperty(0)
    progress = ObjectProperty(None, allownone=True)
    systemCommands = ObjectProperty(None, allownone=True)
    files = ObjectProperty(None, allownone=True)

    profile = ObjectProperty(None, allownone=True)
    profiles = ObjectProperty(None, allownone=True)

    connection = ObjectProperty(None)

    def loadProfiles(self, data = None):
        if data == None:
            response = self.octoprintClient.get("/api/printerprofiles")

            if response.status_code == 200:
                data = response.json()['profiles']
            else:
                return

        if data != None:
            self.profiles = data
            for i in self.profiles:
                if self.profiles[i]['current']:
                    self.profile = self.profiles[i]
                    break

    def loadConnection(self, data = None):
        if data == None:
            response = self.octoprintClient.get("/api/connection")

            if response.status_code == 200:
                data = response.json()
            else:
                return

        if data != None:
            self.connection = data

    def loadTemps(self, data = None):
        if data == None:
            response = self.octoprintClient.get("/api/printer?exclude=state,sd")

            if response.status_code == 200:
                data = response.json()['temperature']
            else:
                return

        if isinstance(data, list) and data != []:
            data = data[0]

        if data != None:
            self.temps = data

    def loadState(self, data = None):
        if data == None:
            response = self.octoprintClient.get("/api/printer?exclude=temperature,sd")

            if response.status_code == 200:
                data = response.json()['state']
            else:
                return

        if data != None:
            self.state = data

    def loadJob(self, data = None):
        if data == None:
            response = self.octoprintClient.get("/api/job")

            if response.status_code == 200:
                data = response.json()['job']
            else:
                return

        if data != None:
            self.job = data

    def loadProgress(self, data = None):
        if data == None:
            response = self.octoprintClient.get("/api/job")

            if response.status_code == 200:
                data = response.json()['progress']
            else:
                return

        if data != None:
            self.progress = data

    def loadSystemCommands(self, data = None):
        if data == None:
            response = self.octoprintClient.get("/api/system/commands")

            if response.status_code == 200:
                data = response.json()
            else:
                return

        if data != None:
            self.systemCommands = data

    def loadFiles(self, data = None):
        if data == None:
            response = self.octoprintClient.get("/api/files")

            if response.status_code == 200:
                data = response.json()
            else:
                return

        if data != None:
            self.files = data

    def loadAll(self):
        self.loadProfiles()
        self.loadConnection()

        response = self.octoprintClient.get("/api/printer")
        if response.status_code == 200:
            data = response.json()
            self.loadTemps(data['temperature'])
            self.loadState(data['state'])

        response = self.octoprintClient.get("/api/job")
        if response.status_code == 200:
            data = response.json()
            self.loadJob(data['job'])
            self.loadProgress(data['progress'])

        self.loadSystemCommands()
        self.loadFiles()

        self.dispatch()

    def sendCommand(self, path, command, data=None):
        self.octoprintClient.post_command(path, command, data)

    def sendDelete(self, path, params=None):
        self.octoprintClient.delete(path, params)

    def on_octoprintConnection(self, inst, value):

        #print(value)

        state = value

        if state == 'Errored':
            #print("Real Errored")
            self.octoprintConnection = 'Reconnecting'
            Clock.schedule_once(self.connect, 1)

        if state == 'Errored' or state == 'Closed':
           #print("Closed or Errored")
            self.logs = []
            self.offesets = []
            self.busyFiles = []
            self.messages = []
            self.state = None
            self.serverTime = 0
            self.temps = None
            self.temp = None
            self.job = None

            self.progress = None
            self.systemCommands = None
            self.files = None
            self.profiles = None
            self.profile = None
            self.connection = None


    def init(self, host, port, apikey):
        Logger.info("Client: Connecting to Octoprint")
        Logger.debug("Client: Host: " + str(host))
        Logger.debug("Client: Port: " + str(port))
        Logger.debug("Client: API Key: " + str(apikey))

        self.octoprintClient = octoprint_client.Client(octoprint_client.build_base_url(https=None, httpuser=None, httppass=None, host=host, port=port, prefix=None), apikey)

        #self.octoprintClient.apikey = apikey
        #self.octoprintClient.baseurl = self.octoprintClient.build_base_url(https=None, httpuser=None, httppass=None, host=host, port=port, prefix=None)

        Clock.schedule_once(self.connect)

    def connect(self, *args):

        if self.socket != None:
            self.socket.disconnect()

       #print(self.octoprintConnection)

        if self.octoprintConnection == 'Reconnecting':
            Logger.warning("Client: Could not connect to Octoprint")
            Logger.warning("Client: Trying to reconnect...")
        else:
            Logger.info("Client: Connecting to Octoprint...")

        def on_connect(ws):
           #print("Connected")
            self.octoprintConnection = 'Connected'
            self.loadAll()

        def on_close(ws):
            #print(self.octoprintConnection)
            if self.octoprintConnection != 'Errored' and self.octoprintConnection != 'Reconnecting':
                self.octoprintConnection = 'Closed'

        def on_error(ws, error):
            self.octoprintConnection = 'Errored'
            #print("Error")

        def on_heartbeat(ws):
            pass

        def on_message(ws, mtype, mdata):
           #print(mtype)
            if mtype == 'current' or mtype == 'history':
                self.logs       = mdata['logs']
                self.offsets    = mdata['offsets']
                self.busyFiles  = mdata['busyFiles']
                self.messages   = mdata['messages']
                self.serverTime = mdata['serverTime']
                #self.currentZ   = mdata['currentZ']

                self.loadState(mdata['state'])
                self.loadTemps(mdata['temps'])
                self.loadJob(mdata['job'])
                self.loadProgress(mdata['progress'])

            if mtype == 'event':
                #print(mdata)

                event = mdata['type']
                payload = mdata['payload']

                if event == 'ClientOpened':
                    self.loadAll()
                if event == 'UpdatedFiles' and payload['type'] == 'printables':
                    self.loadFiles()
                    self.loadJob()
                if event == 'PrinterStateChanged':
                    state = payload['state_id']
                    self.loadState()
                    self.loadJob()
                    if state == 'OFFLINE' or state == 'OPERATIONAL':
                        self.loadConnection()
                        self.loadProfiles()
                if event == 'FileSelected' or event == 'FileDeselected':
                    self.loadJob()
                if event == 'PrintStarted' or event == "PrintFailed" or event == "PrintCancelled" or event == "PrintPaused" or event == "PrintResumed":
                    self.loadProgress()
                    self.loadTemps()
                    self.loadJob()

            if mtype == 'connected':
               #print("Connected")
                self.octoprintConnection = 'Connected'
                self.loadAll()

        self.socket = self.octoprintClient.create_socket(
            on_connect=on_connect,
            on_close=on_close,
            on_error=on_error,
            on_heartbeat=on_heartbeat,
            on_message=on_message
        )

# Data Model
# -----------------------
# u'logs': [u'Recv: wait'],
#  u'messages': [u'wait'],
#  u'offsets': {},
#  u'progress': {u'completion': 0,
#                u'filepos': None,
#                u'printTime': None,
#                u'printTimeLeft': None},
#  u'serverTime': 1478129383.582231,
#  u'state': {u'flags': {u'closedOrError': False,
#                        u'error': False,
#                        u'operational': True,
#                        u'paused': False,
#                        u'printing': False,
#                        u'ready': True,
#                        u'sdReady': True},
#             u'text': u'Operational'},
#  u'temps': []}
# {u'busyFiles': [],
#  u'currentZ': None,
#  u'job': {u'averagePrintTime': None,
#           u'estimatedPrintTime': 1738.1001096946788,
#           u'filament': {u'tool0': {u'length': 2852.840489999994,
#                                    u'volume': 6.861885524017607}},
#           u'file': {u'date': 1477691593,
#                     u'name': u'Aquabot_Wall.gcode',
#                     u'origin': u'local',
#                     u'path': u'Aquabot_Wall.gcode',
#                     u'size': 665276},
#           u'lastPrintTime': None},
# --------------------------
# u'logs': [u'Recv: ok T:145.15 /200.00 B:1.00 /1.00 @:64'],
#  u'messages': [u'ok T:145.15 /200.00 B:1.00 /1.00 @:64'],
#  u'offsets': {},
#  u'progress': {u'completion': None,
#                u'filepos': None,
#                u'printTime': None,
#                u'printTimeLeft': None},
#  u'serverTime': 1478211770.371015,
#  u'state': {u'flags': {u'closedOrError': False,
#                        u'error': False,
#                        u'operational': True,
#                        u'paused': False,
#                        u'printing': False,
#                        u'ready': True,
#                        u'sdReady': True},
#             u'text': u'Operational'},
#  u'temps': [{u'bed': {u'actual': 1.0, u'target': 1.0},
#              u'time': 1478211769,
#              u'tool0': {u'actual': 145.15, u'target': 200.0}}]}
# {u'busyFiles': [],
#  u'currentZ': None,
#  u'job': {u'estimatedPrintTime': None,
#           u'filament': {u'length': None, u'volume': None},
#           u'file': {u'date': None,
#                     u'name': None,
#                     u'origin': None,
#                     u'path': None,
#                     u'size': None},
#           u'lastPrintTime': None},
