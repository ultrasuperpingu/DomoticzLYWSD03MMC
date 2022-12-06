# DomoticzLYWSD03MMC
Xiaomi Mijia Humidity and Temperature (LYWSD03MMC) plugin for Domoticz.

This plugin IS FLAWED (look at the issues to know more about it). I DON'T RECOMMAND TO USE IT.

*Read this in french: [Français](README.fr.md)*
## Installation
Requirements: Only tested with Domoticz version 2020.2, Python 3 have to be installed.
* Install required python packages:
   - ```sudo apt-get install python3-pip libglib2.0-dev```
   - ```sudo apt-get install --no-install-recommends bluetooth```
   - ```sudo pip3 install gatt```
   - ```sudo apt-get install python3-dbus```
 
To get the development version:
* With command line, go to Domoticz's plugin directory (domoticz/plugins)
* Launch: ```git clone https://github.com/ultrasuperpingu/DomoticzLYWSD03MMC.git```
* Restart Domoticz service: ```sudo service domoticz restart```

You also can copy the plugin.py file in directory ```domoticz/plugins/{ChooseYourDirectoryName}``` and restart domoticz.

To get a release version (when there will be one), download it and uncompress it in the ```domoticz/plugins/{ChooseYourDirectoryName}``` directory and restart domoticz.

## Update

To update the plugin:

* With command line, go to Domoticz's plugin directory (domoticz/plugins)
* Launch: ```git pull```
* Restart Domoticz service: ```sudo service domoticz restart```

You can also update the plugin.py file in directory ```domoticz/plugins/{ChooseYourDirectoryName}``` and restart domoticz.

## Configuration
 * Get your sensor's MAC address:
   - ```sudo hcitool lescan```
   - Search a line looking like: ```A1:C2:E3:04:25:46 LYWSD03MMC```
 * Enter MAC address in the corresponding field in plugin parameters
 * Enter Adapter name (default is hci0)
