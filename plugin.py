"""
Xiaomi Mijia LYWSD03MMC Bluetooth 4.2 Temperature Humidity sensor python plugin for Domoticz
Author: Ultrasuperpingu,
		adapted from Reading data from Xiaomi Mijia LYWSD03MMC Bluetooth 4.2 Temperature Humidity sensor, see:
			https://github.com/trandbert37/DomoticzMiTemperature2
Version: 0.3 (January, 2022)
"""
"""
<plugin key="LYWSD03MMC" name="Xiaomi Mijia Humidity and Temperature (LYWSD03MMC)" author="ulstrasuperpingu" version="0.1" externallink="https://github.com/ultrasuperpingu/DomoticzLYWSD03MMC">
	<description>
		<h2>Xiaomi Mijia Humidity and Temperature (LYWSD03MMC) for Domoticz</h2><br/>
		Retreive data from Xiaomi Mijia LYWSD03MMC Humidity and Temperature sensor
		<h3>Set-up and Configuration</h3>
		Install bluepy module: <pre>sudo apt-get install --no-install-recommends bluetooth
sudo pip3 install gatt
sudo apt-get install python3-dbus</pre><br/>
		Find the MAC adress of your sensor: <pre>sudo hcitool lescan</pre> <br/>
		<small>Look for lines like <pre>A1:C2:E3:04:25:47 LYWSD03MMC</pre></small><br/>
		Change Adapter name if needed (default is hci0).<br/>
		Set the MAC adresses (comma (',') separated) in the plugin parameters and add the hardware.
	</description>
	<params>
		<param field="Mode1" label="Adapter name" width="120px" required="true" default="hci0"/>
		<param field="Mode2" label="MAC Adresses" width="250px" line="3" required="true" default=""/>
	</params>
</plugin>
"""

import Domoticz
import gatt
import re
import math
from datetime import datetime, timedelta
from threading import Thread

class LYWSD03MMCDevice(gatt.Device):
	def __init__(self, mac_address, manager, plugin):
		gatt.Device.__init__(self, mac_address=mac_address, manager=manager)
		self.plugin = plugin
		self.temp = 0
		self.humidity = 0
		self.batt = 0
		self.received = False
		self.receivedBatt = False
		
	def connect_succeeded(self):
		super().connect_succeeded()
		Domoticz.Log("[%s] Connected" % (self.mac_address))

	def connect_failed(self, error):
		super().connect_failed(error)
		Domoticz.Log("[%s] Connection failed: %s" % (self.mac_address, str(error)))

	def disconnect_succeeded(self):
		super().disconnect_succeeded()
		Domoticz.Log("[%s] Disconnected" % (self.mac_address))

	def services_resolved(self):
		super().services_resolved()

		Domoticz.Log("[%s] Resolved services" % (self.mac_address))
		for service in self.services:
			Domoticz.Log("[%s]  Service [%s]" % (self.mac_address, service.uuid))
			for characteristic in service.characteristics:
				Domoticz.Log("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))
				characteristic.read_value()
				if characteristic.uuid == 'ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6' or characteristic.uuid == 'ebe0ccc4-7a0a-4b0c-8a1a-6ff2997da3a6':
					characteristic.enable_notifications()

	def characteristic_value_updated(self, characteristic, value):
		if characteristic.uuid == '00002a26-0000-1000-8000-00805f9b34fb':
			print("Firmware version: "+value.decode("utf-8"))
		elif characteristic.uuid == 'ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6':
			self.temp=int.from_bytes(value[0:2],byteorder='little',signed=True)/100
			self.humidity=int.from_bytes(value[2:3],byteorder='little')
			self.received = True
			print(characteristic.uuid+":"+str(self.plugin.temp)+" "+str(self.plugin.humidity))
		elif characteristic.uuid == 'ebe0ccc4-7a0a-4b0c-8a1a-6ff2997da3a6':
			self.batt = int.from_bytes(value,byteorder="little")
			self.receivedBatt = True
		elif len(value) == 4:
			print(characteristic.uuid+":"+str(int.from_bytes(value,byteorder="little")))
		else:
			print(characteristic.uuid+":"+str(value))
			
class BasePlugin:

	def __init__(self):
		self.temp = 0
		self.humidity = 0
		self.batt = 0
		self.validConf = False
		self.thread = None
		self.received = False
		self.receivedBatt = False
		return


	def onStart(self):
		# create the child devices if these do not exist yet
		self.devices = []
		
		self.manager = gatt.DeviceManager(adapter_name=Parameters["Mode1"])
		addresses = Parameters["Mode2"].split(',');
		self.validConf = True;
		id=1
		for add in addresses:
			if not re.match("[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$", add):
				self.validConf = False
			else:
				if id not in Devices:
					Domoticz.Status("Creating Temp+Hum device for mac "+add)
					Domoticz.Device(Name="Temp+Humidity ("+add+")", Unit=id, Type=82, Subtype=1, Used=1).Create()
				device = LYWSD03MMCDevice(mac_address=add, manager=self.manager, plugin=self)
				device.connect()
				self.devices += [device]
				id+=1
			
		if not self.validConf:
			Domoticz.Error("Please specify device MAC addresses in format AA:BB:CC:DD:EE:FF")
			return
		
		self.thread = Thread(target = lambda : self.manager.run())
		self.thread.start()
		


	def onStop(self):
		if self.thread and self.thread.is_alive():
			self.manager.stop()
			self.thread.join()
			self.manager = None
			self.thread = None
		self.devices=[]

	def onCommand(self, Unit, Command, Level, Color):
		Domoticz.Log("onCommand called for Unit {}: Command '{}', Level: {}".format(Unit, Command, Level))


	def onHeartbeat(self):
		if not self.validConf:
			return
		id=1
		for d in self.devices:
			if d.received:
				Devices[id].Update(nValue=0, sValue=str(d.temp)+";"+str(d.humidity)+";0")
				d.received = False
			if d.receivedBatt:
				Devices[id].Update(nValue=0, sValue=str(d.temp)+";"+str(d.humidity)+";0", BatteryLevel=d.batt)
				d.receivedBatt = False
			if not d.is_connected():
				d.connect()
			id+=1



global _plugin
_plugin = BasePlugin()


def onStart():
	global _plugin
	_plugin.onStart()


def onStop():
	global _plugin
	_plugin.onStop()


def onCommand(Unit, Command, Level, Color):
	global _plugin
	_plugin.onCommand(Unit, Command, Level, Color)


def onHeartbeat():
	global _plugin
	_plugin.onHeartbeat()

