# Installation

## Raspberry Pi with Official Display and Raspbian Lite

***Any reference to `python` or `pip` should be replaced with the correct path from the python virtual envirnment that Octoprint was installed in.***

If you followed the official Octoprint installation instructions for the Pi, this would be `/home/pi/OctoPrint/venv/bin/python` and `/home/pi/OctoPrint/venv/pip`.

I believe that for OctoPi, it is in the `oprint` directory

Make sure that Octoprint is installed, even if you will be connecting to an Octoprint instance on another computer.
Octoscreen uses the `octoprint_client` module that is bundled with Octoprint

------

Make sure the system is updated
```
sudo apt-get update
sudo apt-get upgrade
```

Make sure `git` is installed
```
sudo apt-get install git
```

Install Kivy dependancies
```
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev cython
   
pip install cython
```

Install Kivy
```
pip install git+https://github.com/kivy/kivy.git@master
```
Install Octoscreen
```
cd ~
pip install websocket-client
git clone https://github.com/chickenchuck040/octoscreen
```

Run Octoscreen for the first time
```
cd ~/octoscreen
python main.py
```
Touch does not work at this point.
Install the touch driver
```
sudo apt-get install libmtdev1
```

Open `~/.kivy/config.ini`
```
nano ~/.kivy/config.ini
```

Add these lines to the `[input]` section
```
mouse = mouse
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput
```

Run Octoscreen again
```
cd ~/octoscreen
python main.py
```
Everything should work now. 
Hit the gear button at the top and change the API key for your Octoprint, as well as the address and port if needed.
An address of `127.0.0.1` will connect to a local Octoprint, and a port of `5000` is the default Octoprint port.

