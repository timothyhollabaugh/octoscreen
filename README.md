Octoscreen
===

Octoscren is a touchscreen interface for [Octoprint](https://github.com/foosel/OctoPrint), designed for the official [Raspberry Pi Touchscreen](https://www.raspberrypi.org/products/raspberry-pi-touch-display/). It is currently in a very useable state, but is still under developement.

This uses a websocket and REST API to talk to Octoprint. It uses the [octoprint_client](https://github.com/foosel/OctoPrint/tree/master/src/octoprint_client) module that comes with Octoprint to handle the websocket and REST API. It currently requires Octoprint to be installed, but it may connect to an Octoprint on another system.

Octoscren uses [Kivy](http://kivy.org/#home) to draw to the screen and handle input. Kivy provides a nice way to do GPU accelerated graphics, while still remaining portable to other systems.

Octoscreen is designed for the Raspberry Pi Touchscreen, however it should work anywhere Kivy is supported. If using a screen of a different size, you should change the `height` and `width` config options in `main.py`.
```
Config.set('graphics', 'height', '480')
Config.set('graphics', 'width', '800')
```

Features
===
**Stable, fully functioning features**

 - View status of the printer, including:
  - Current state
  - Current file loaded
  - Temperatures
  - Filament usage for the current file loaded
  - Time into print
  - Time remaining in print
  - Total time of print
  - Start, stop, or cancel prints
  
  ![Status Picture](https://raw.githubusercontent.com/chickenchuck040/octoscreen/master/screenshots/status_printing.png)
  
 - Control of the printer, including:
  - Temperatures with a nice on screen keypad
  - Tool selection
  - Filament extrude/retract of different amounts
  - Motors on/off
  - Jog with different step sizes
  - Home XY, Z, or XYZ
  
  ![Printer Picture](https://raw.githubusercontent.com/chickenchuck040/octoscreen/master/screenshots/printer.png)
  
 - Connection and other miscellaneous controls, including:
  - Serial port, baud rate, and profile selection for connecting
  - Any commands configued in the System menu. It uses breaks to seperate the buttons on different lines.
 - File Selector for files uploaded to Octoprint:
  - Shows files in date order, newest at the top
  - Shows date uploaded and estimated time
  - Allows printing, selecting, or deleting a file
  
  ![Files Picture](https://raw.githubusercontent.com/chickenchuck040/octoscreen/master/screenshots/files.png)
  
 - Adjusts displayed information to match printer profile:
  - Number of extruders
  - Heated Bed temperatures
 - Settings menu to configure Octoprint URL, Port, and API Key, and other Kivy settings
 
  ![Settings Picture](https://raw.githubusercontent.com/chickenchuck040/octoscreen/master/screenshots/settings.png)

Upcoming Features
===
**Features to maybe get into a future commit**

 - Settings in Octoprint settings manager
 - Custom buttons
 - Terminal tab
 - Gcode viewer
 - Slicer tab

Installation
===

First, make sure that [Octoprint](https://github.com/foosel/OctoPrint) is installed

Install [Kivy](http://kivy.org/#home)
Use the instructions [here](https://kivy.org/docs/installation/installation-rpi.html) for installation on a Raspberry Pi.

Install the `websocket-client` module
```
pip install --user websocket-client
```

Make sure that the correct `python` is being run if Octoprint is in a virtual environment (ie OctoPi)
```
git clone https://github.com/chickenchuck040/octoscreen.git
cd octoscreen
```

Run it with
```
python main.py
```

It would be wise to write a systemd service file to start it on boot.
