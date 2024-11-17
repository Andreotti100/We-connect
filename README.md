Domoticz plugin to read my VW ID.3 battery percentage and distance left.

Uses: Python API for the Volkswagen WeConnect Services
URL: https://github.com/tillsteinbach/WeConnect-python

Setup We-connect API on Raspberry Pi:

apt install python3-pip
pip3 install weconnect-cli

When you get this error: "externally-managed-environment"
pip3 install weconnect-cli --break-system-packages

Test:
weconnect-cli --username 'email' --password 'my_password'

Known issue: The check for the right VIN is not working for some reason!


The timer component in the weconnect-cli API failes at converting the date/time if it is called from Domoticz. Maybe it has to do with my region notation.
So, I changed some code.
  Open /usr/local/lib/python3.11/dist-packages/weconnect/elements/timer.py
  Go to line 97

        def update(self, fromDict):  # noqa: C901
            LOG.debug('Update recurring timer from dict')

            # this fails in my Domoticz plugin:
            # --------------------------------->
            # if 'startTime' in fromDict:
            #     self.startTime.setValueWithCarTime(datetime.strptime(f'{fromDict["startTime"]}+00:00', '%H:%M%z'),
            #                                        lastUpdateFromCar=None, fromServer=True)
            # else:
            #     self.startTime.enabled = False
            # 
            # if 'targetTime' in fromDict:
            #     self.targetTime.setValueWithCarTime(datetime.strptime(f'{fromDict["targetTime"]}+00:00', '%H:%M%z'),
            #                                         lastUpdateFromCar=None, fromServer=True)
            # else:
            #     self.targetTime.enabled = False
            # <---
            # No need for time in Domoticz:
            self.startTime.enabled = False
