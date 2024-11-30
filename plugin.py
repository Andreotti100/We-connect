# We-connect - Volkswagen group - Domoticz plugin
# Tested with my VW ID.3
#
# Author: Andreotti 2024
#
# Uses: Python API for the Volkswagen WeConnect Services
# Web: https://github.com/tillsteinbach/WeConnect-python
#
# Setup We-connect API on Raspberry Pi
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# apt install python3-pip
# pip3 install weconnect-cli
#
# When you get this error: "externally-managed-environment"
# pip3 install weconnect-cli --break-system-packages
#
# Test:
# weconnect-cli --username 'email' --password 'my_password'
#
# P.S. the check for the right VIN is not working for some reason!

"""
<plugin key="We-connect" name="We-connect" author="Andreotti" version="1.0.1" >
  <description>
    <p>
    VIN is optional. Use it if you have more then one car connected in your app.<br/>
    On error, login again at: https://id.vwgroup.io/
    </p>
    Credentials:
  </description>
  <params>
    <param field="Username" label="Username" width="150px"/>
    <param field="Password" label="Password" width="150px" default="" password="true"/>
    <param field="VIN" label="VIN (optional)" width="150px"/>
  </params>
</plugin>
"""

import Domoticz
from weconnect import weconnect

class BasePlugin:

  runAgain = 1
  weConnect = None

  def __init__(self):
    return

  def onStart(self):

    self.weConnect = weconnect.WeConnect(username=Parameters["Username"], password=Parameters["Password"], updateAfterLogin=False, loginOnInit=False)
    if (self.weConnect):
      try:
        self.weConnect.login()
      except Exception as e:
        Domoticz.Log(f"Error during weConnect update: {str(e)}")
        return

    if len(Devices) == 0:
      Domoticz.Device(Name="Battery", Unit=1, Type=243, Subtype=6, Switchtype=0).Create()
      Domoticz.Device(Name="Distance", Unit=2, TypeName="Custom", Options={"Custom": "1;km"}).Create()

      Domoticz.Log("Created device: ")

  def onStop(self):
    return

  def onDisconnect(self, Connection):
    return

  def onHeartbeat(self):
    self.runAgain = self.runAgain - 1
    if (self.runAgain > 0):
      return

    self.runAgain = 60  # 1x per 5 minuten checken (60 x 5 sec)

    if (self.weConnect):
      try:
        self.weConnect.update()
      except Exception as e:
        Domoticz.Log(f"Error during weConnect update: {str(e)}")
        return

      try:
        for vin, vehicle in self.weConnect.vehicles.items():
          # if (Parameters["VIN"] == "" or vin == Parameters["VIN"]):
            if "charging" in vehicle.domains and "batteryStatus" in vehicle.domains["charging"]:
              Devices[1].Update(nValue=0, sValue=str(vehicle.domains["charging"]["batteryStatus"].currentSOC_pct.value))
              Devices[2].Update(nValue=0, sValue=str(vehicle.domains["charging"]["batteryStatus"].cruisingRangeElectric_km.value))

      except Exception as e:
        Domoticz.Log(f"Error reading weConnect data: {str(e)}")
        return

global _plugin
_plugin = BasePlugin()

def onStart():
  global _plugin
  _plugin.onStart()

def onStop():
  global _plugin
  _plugin.onStop()

def onDisconnect(Connection):
  global _plugin
  _plugin.onDisconnect(Connection)

def onHeartbeat():
  global _plugin
  _plugin.onHeartbeat()

