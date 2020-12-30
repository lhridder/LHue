# LHue main
# imports
import configparser
import sys
import os
import requests

ip = ""
key = ""
base = ""


# check config
def createconfig():
    print('Checking if config exists...')
    # check file
    try:
        file = open("config.ini")
        # Do something with the file
        file.close()
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
    print("Config exists. continuing...")


# load config
def loadconfig():
    global ip, key, base
    config = configparser.ConfigParser()
    config.read("config.ini")
    ip = config["HUEBRIDGE"]["ip"]
    key = config["HUEBRIDGE"]["key"]
    base = "http://" + ip + "/api/" + key + "/"


# ping hue / Checks if Hue online
def checkonline():
    response = os.system("ping -n 1 " + ip)

    # and then check the response...
    if response == 0:
        print('Hue bridge online, continuing')
    else:
        print('Hue bridge offline, stopping')
        sys.exit(0)  # stops if offline

    # check key
    r = requests.get('http://' + ip + "/api/" + key)
    if r.text.__contains__("unauthorized"):
        print('Hue bridge api-key not authorized, quitting')
        sys.exit(0)
    else:
        print("Authorized")


# get lamp info
def getinfo(lamp=None):
    # get all lights
    if lamp is None:
        print("get all light info")
        r = requests.get(base)
        # format json
        rjson = r.json()
        # get lights
        lights = rjson["lights"]
        # get every light
        for k, v in lights.items():
            print("Lamp " + k + ":")
            print("  Name: " + str(lights[k]["name"]))
            print("  On: " + str(lights[k]["state"]["on"]))
            print("  Hue: " + str(lights[k]["state"]["hue"]))
            print("  Brightness: " + str(lights[k]["state"]["bri"]))
    # get one light
    else:
        print("get light " + lamp + " info")


# turn on/off
def togglelight(lamp, boolean):
    print("Setting lamp " + str(lamp) + " to " + boolean)
    # form url
    url = base + "lights/" + str(lamp) + "/state"
    # form body
    body = '{"on":' + boolean + '}'
    r = requests.put(url, body)
    # format response
    rjson = r.json()
    print(rjson)
    # filter response
    response = rjson[0]["success"]
    for k, v in response.items():
        # filter lamp no
        lamp = k.replace("/lights/", "").replace("/state/on", "")
        # filter lamp status
        if v:
            status = "on"
        else:
            status = "off"
        # print result
        print("lamp " + lamp + " is now " + status)


# zet brightness
def setbrightness(lamp, brightness):
    print("Setting lamp ", str(lamp), " to brightness: ", brightness)
    # form url
    url = base + "lights/" + str(lamp) + "/state"
    # form body
    body = '{"bri":' + str(brightness) + '}'
    r = requests.put(url, body)
    # format response
    rjson = r.json()
    # print(rjson)
    # filter response
    response = rjson[0]["success"]
    for k, v in response.items():
        # filter lamp no
        lamp = k.replace("/lights/", "").replace("/state/bri", "")
        # print result
        print("lamp " + lamp + " brightness is now " + str(v))


# zet kleur
def setcolor(lamp, color):
    print("setting lamp 1 to " + str(color))
    url = base + "lights/" + str(lamp) + "/state"
    body = '{"hue":' + str(color) + '}'
    r = requests.put(url, body)
    # format response
    rjson = r.json()
    response = rjson[0]["success"]
    print(rjson)
    # light = rjson["lights"][1]
    for k, v in response.items():
        # filter lamp no
        lamp = k.replace("/lights/", "").replace("/state/hue", "")
        # print result
        print("lamp " + lamp + " hue is now " + str(v))


# main script
if __name__ == '__main__':
    print('LHue starting')
    # create config
    createconfig()
    # load config
    loadconfig()
    # continue huts
    checkonline()
    # get all lamp info
    getinfo()
    # huts lamp aan
    togglelight(1, "true")
    # zet brightness
    setbrightness(1, 254)
    # zet kleur
    setcolor(1, 40000)
