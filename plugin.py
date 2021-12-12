"""
Xiaomi Mijia LYWSD03MMC Bluetooth 4.2 Temperature Humidity sensor python plugin for Domoticz
Author: Ultrasuperpingu,
		adapted from Reading data from Xiaomi Mijia LYWSD03MMC Bluetooth 4.2 Temperature Humidity sensor, see:
			https://github.com/trandbert37/DomoticzMiTemperature2
Version: 0.1 (December, 2021) - see history.txt for versions history
"""
"""
<plugin key="LYWSD03MMC" name="Xiaomi Mijia Humidity and Temperature (LYWSD03MMC)" author="ulstrasuperpingu" version="0.1" externallink="https://github.com/ultrasuperpingu/DomoticzLYWSD03MMC">
	<description>
		<h2>Xiaomi Mijia Humidity and Temperature (LYWSD03MMC) for Domoticz</h2><br/>
		Retreive data from Xiaomi Mijia LYWSD03MMC Humidity and Temperature sensor
		<h3>Set-up and Configuration</h3>
		Install bluepy module: <pre>sudo pip3 install requests bluepy</pre><br/>
		Find the MAC adress of your sensor: <pre>sudo hcitool lescan</pre> <br/>
		<small>Look for lines like <pre>A1:C2:E3:04:25:47 LYWSD03MMC</pre></small><br/>
		Set the MAC adress in the plugin parameters and add the hardware.
	</description>
	<params>
		<param field="Mode1" label="MAC Adress" width="120px" required="true" default=""/>
		<param field="Mode2" label="Battery request time (in minutes)" width="120px" default="1440"/>
	</params>
</plugin>
"""

import Domoticz
from bluepy import btle
import re
import math
from datetime import datetime, timedelta

mode="round"
class MyDelegate(btle.DefaultDelegate):
	def __init__(self, plug):
		btle.DefaultDelegate.__init__(self)
		self.plugin = plug
	
	def handleNotification(self, cHandle, data):
		try:
			self.plugin.temp=int.from_bytes(data[0:2],byteorder='little',signed=True)/100
			self.plugin.humidity=int.from_bytes(data[2:3],byteorder='little')
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			self.plugin.p.disconnect()
			self.plugin.p = None

class BasePlugin:

	def __init__(self):
		self.temp = 0
		self.humidity = 0
		self.lastBattUpdate = None
		self.batteryRequestTime = 1440
		self.p=None
		self.validConf = False
		return


	def onStart(self):
		# create the child devices if these do not exist yet
		devicecreated = []
		if 1 not in Devices:
			Domoticz.Status("Creating Temp+Hum device")
			Domoticz.Device(Name="Temp+Humidity", Unit=1, Type=82, Subtype=1, Used=1).Create()
			
		try:
			self.batteryRequestTime = int(Parameters["Mode2"])
		except ValueError:
			self.batteryRequestTime = 1440
			Domoticz.Error("Invalid battery request time: set it to default 1440")
			
		if re.match("[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$", Parameters["Mode1"]):
			self.adress=Parameters["Mode1"]
			self.validConf = True
		else:
			Domoticz.Error("Please specify device MAC-Address in format AA:BB:CC:DD:EE:FF")


	def onStop(self):
		if self.p:
			self.p.disconnect()


	def onCommand(self, Unit, Command, Level, Color):
		Domoticz.Log("onCommand called for Unit {}: Command '{}', Level: {}".format(Unit, Command, Level))


	def onHeartbeat(self):
		if not self.validConf:
			return
		if not self.p:
			try:
				self.connectBluetooth();
			except btle.BTLEException:
				Domoticz.Error("Unable to connect to " + self.adress)
			return
		try:
			if self.p.waitForNotifications(500):
				now = datetime.now()
				if not self.lastBattUpdate or self.lastBattUpdate + timedelta(minutes=self.batteryRequestTime) < now:
					Domoticz.Status("Reading battery level...")
					batt=self.p.readCharacteristic(0x001b)
					batt=int.from_bytes(batt,byteorder="little")
					Devices[1].Update(nValue=0, sValue=str(self.temp)+";"+str(self.humidity)+";0", BatteryLevel=batt)
					self.lastBattUpdate=now
				else:
					Devices[1].Update(nValue=0, sValue=str(self.temp)+";"+str(self.humidity)+";0")
		except btle.BTLEException :
			Domoticz.Error("Disconnect from " + self.adress)
			try:
				self.p.disconnect()
			except Exception:
				pass
			self.p = None
		
	def connectBluetooth(self):
		Domoticz.Status("Connecting bluetooth ...")
		self.p = btle.Peripheral(self.adress)
		val=b'\x01\x00'
		self.p.writeCharacteristic(0x0038,val,True)
		self.p.withDelegate(MyDelegate(self))
		Domoticz.Status("Connected")
		return self.p



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

