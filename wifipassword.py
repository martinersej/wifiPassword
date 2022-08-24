#! py
#################################################################################
# Copyright of David Bombal, 2021                                               #
# https://www.davidbombal.com                                                   #
# https://www.youtube.com/davidbombal                                           #
# https://github.com/davidbombal/red-python-scripts/blob/main/windows10-wifi.py #
#################################################################################

#What did I do with that source code?
#I Made some few changes.

import subprocess
import re
from sys import platform
from unittest import skip

if __name__ == '__main__':
    if platform == "linux" or platform == "linux2":
        skip
    elif platform == "darwin":
        command_output = subprocess.run(["networksetup", "-listpreferredwirelessnetworks", "en0"], capture_output=True, stdin=subprocess.DEVNULL).stdout.decode()
        profile_names = (re.findall("\t(.*)", command_output))
        if len(profile_names) != 0:
            listWifi = []
            for name in profile_names:
                wifiProfile = {}
                profileInfoPasswd = subprocess.run(["security", "find-generic-password", "-D", "'AirPort network password'", "-ga", '\"{}\"'.format(name)], capture_output = True, stdin=subprocess.DEVNULL).stdout.decode()
                print(profileInfoPasswd)
                if re.search("password: (.*)\r", profileInfoPasswd) == None:
                    wifiProfile["ssid"] = name
                    password = re.search("password: (.*)\r", profileInfoPasswd)
                    wifiProfile["password"] = password if password != None else None
                    listWifi.append(wifiProfile)
    elif platform == "win32":
        command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, stdin=subprocess.DEVNULL).stdout.decode()
        profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
        if len(profile_names) != 0:
            listWifi = []
            for name in profile_names:
                wifiProfile = {}
                profileInfo = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True, stdin=subprocess.DEVNULL).stdout.decode()
                if re.search("Security key           : Absent", profileInfo) == None:
                    wifiProfile["ssid"] = name
                    profileInfoPasswd = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True, stdin=subprocess.DEVNULL).stdout.decode()
                    password = re.search("Key Content            : (.*)\r", profileInfoPasswd)
                    wifiProfile["password"] = password[1] if password != None else None
                    listWifi.append(wifiProfile)
    listWifi.sort(key=lambda x: x['ssid'])
    for x in range(len(listWifi)):
        print('Name: {}, Password: {}'.format(listWifi[x]['ssid'], listWifi[x]['password']))
