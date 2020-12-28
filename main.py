# LHue main
# imports
import configparser
import sys
import os
import requests

ip = ""
key = ""


# check config
def createconfig():
    print('Checking if config exists...')
    # check file
    try:
        f = open("config.ini")
        # Do something with the file
        f.close()
    except IOError:
        print("Config file doesn't exist yet, making one...")
        # make config
        config = configparser.ConfigParser()
        config['HUEBRIDGE'] = {'ip': '', 'key': ''}
        # write to config
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        # config created
        print("Config created! stopping...")
        sys.exit(0)
    # config exists
    print("Config exists. continueing...")


# load config
def loadconfig():
    global ip, key
    config = configparser.ConfigParser()
    config.read("config.ini")
    ip = config["HUEBRIDGE"]["ip"]
    key = config["HUEBRIDGE"]["key"]


# ping hue
def checkonline():
    response = os.system("ping -n 1 " + ip)

    # and then check the response...
    if response == 0:
        print('Hue bridge online, continueing')
    else:
        print('Hue bridge offline, stopping')
        sys.exit(0)

    # check key
    r = requests.get('http://' + ip + "/api/" + key)
    if r.text.__contains__("unauthorized"):
        print('Hue bridge api-key not authorized, quitting')
        sys.exit(0)
    else:
        print("Huts")

    rjson = r.json()
    lights = rjson["lights"]
    for k, v in lights.items():
        print("Lamp " + k + ":")
        print("  Name: " + str(lights[k]["name"]))
        print("  On: " + str(lights[k]["state"]["on"]))
        print("  Hue: " + str(lights[k]["state"]["hue"]))
        print("  Brightness: " + str(lights[k]["state"]["bri"]))


# main script
if __name__ == '__main__':
    print('LHue starting')
    # create config
    createconfig()
    # load config
    loadconfig()
    # continue huts
    checkonline()
