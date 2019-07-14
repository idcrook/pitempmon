pitempmon
=========

Log Raspberry Pi CPU temperatures (to phant)

install
-------

```
# clone repo
mkdir ~/projects
cd ~/projects
git clone --recurse-submodules https://github.com/idcrook/pitempmon.git
cd pitempmon

# install requirements (using a virtualenv)
python3 -m venv env
source env/bin/activate
pip install wheel
pip install requests
pip install RPi.GPIO
pip install gpiozero

# install from local submodule clone
cd python3-phant
pip install -e .
```

### systemd service

There is

configure
---------

```
cp   app_config.example.json   app_config.secrets.json
cp phant-config.example.json phant-config.secrets.json
# EDIT the files
source env/bin/activate
which python
# should be one in ./env/bin/python

# now can run
python ./pitemplog.py
```

inspired by
-----------

-	Adafruit Blog [Logging Raspberry Pi 4 CPU Temperature Data using Adafruit IO #RaspberryPi #IoTuesday #DesktopPiChallenge @AdafruitIO @Raspberry_Pi](https://blog.adafruit.com/2019/07/09/logging-raspberry-pi-4-cpu-temperature-data-using-adafruit-io-raspberrypi-iotuesday-desktoppichallenge-adafruitio-raspberry_pi/)
	-	https://github.com/darrell24015/tempmon

repo initialization
-------------------

```
git submodule add -b master https://github.com/idcrook/python3-phant.git
git add python3-phant

# on fresh clones
git submodule update --init --recursive
```
