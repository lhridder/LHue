# LHue main
# imports
import configparser
import sys
import time
import csv


import requests

ip = ""
key = ""
base = ""
normaal = 8400


# check config bestand
def checkconfig():
    # Kijk of bestand bestaat
    try:
        file = open("config.ini")
        # Bestand bestaat, dus sluiten
        file.close()
    except IOError:
        print("Config file doesn't exist yet, making one...")
        # make config
        config = configparser.ConfigParser()
        config['HUEBRIDGE'] = {'ip': '', 'key': ''}
        # Schrijf waardes naar bestand
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("Config created! stopping...")
        sys.exit(0)
    # config bestaat, ga verder met het programma
    print("Config exists. continuing...")


# load config
def loadconfig():
    global ip, key, base
    config = configparser.ConfigParser()
    config.read("config.ini")
    # krijg de ip en api-key variabelen
    ip = config["HUEBRIDGE"]["ip"]
    key = config["HUEBRIDGE"]["key"]
    # maak de basis url
    base = "http://" + ip + "/api/" + key + "/"


# Kijk of API-key klopt
def checkonline():
    # check key
    r = requests.get('http://' + ip + "/api/" + key)
    if r.text.__contains__("unauthorized"):
        print('Hue bridge api-key not authorized, quitting')
        sys.exit(0)
    else:
        print("Authorized")


# Krijg info over de lampen
def getlampinfo(lamp=None):
    # Krijg info over alle lampen
    if lamp is None:  # Als in mainscript getinfo(), pakt hij info van alle lampen
        print("get all light info")
        r = requests.get(base)
        # format json
        rjson = r.json()
        # get lights
        lights = rjson["lights"]
        # get every light
        for k, v in lights.items():
            print("Lamp " + k + ":")
            print("  Name: " + str(lights[k]["name"]))  # print de naam van de lamp
            print("  On: " + str(lights[k]["state"]["on"]))  # print of de lamp aan staat
            print("  Hue: " + str(lights[k]["state"]["hue"]))  # print de kleurcode van de lamp
            print("  Brightness: " + str(lights[k]["state"]["bri"]))  # print de felheid van de lamp
    # Krijg info over specifieke lamp
    else:  # Als in mainscript getinfo(1), pakt hij info van een specifieke lamp
        print("get light " + str(lamp) + " info")
        url = base + "lights/" + str(lamp)
        r = requests.get(url)
        # format json
        rjson = r.json()
        # print info van lamp
        print("Lamp " + str(lamp) + ":")
        print("  Name: " + str(rjson["name"]))  # print de naam van de lamp
        print("  On: " + str(rjson["state"]["on"]))  # print of de lamp aan staat
        print("  Hue: " + str(rjson["state"]["hue"]))  # print de kleurcode van de lamp
        print("  Brightness: " + str(rjson["state"]["bri"]))  # print de felheid van de lamp


# get sensor data
def getmotionsensor():
    url = base + "sensors/4"
    r = requests.get(url)
    # format json
    rjson = r.json()
    print(rjson)
    name = str(rjson["name"])
    presence = str(rjson["state"]["presence"])
    lastupdated = str(rjson["state"]["lastupdated"])
    # print sensor info
    print("Sensor 1:")
    print("  Name: " + name)
    print("  Presence: " + presence)
    print("  Last presence change: " + lastupdated)
    # Als er iemand aanwezig is gaat de lamp aan, sensor checkt dan minder vaak
    if presence == "True":
        togglelight(1, "true")
        setbrightness(1, 254)
        setcolor(1, normaal)
        time.sleep(15)
    # als er niemand meer aanwezig is gaat het licht uit.
    else:
        togglelight(1, "false")


def getambientlightsensor():
    url = base + "sensors/5"
    r = requests.get(url)
    # format json
    rjson = r.json()
    # get data from json
    name = str(rjson["name"])
    lightlevel = str(rjson["state"]["lightlevel"])
    dark = str(rjson["state"]["dark"])
    daylight = str(rjson["state"]["daylight"])
    lastupdated = str(rjson["state"]["lastupdated"])
    # print sensor info
    print("Sensor 1:")
    print("  Name: " + name)
    print("  Light level: " + lightlevel)
    print("  Daylight: " + daylight)
    print("  Dark: " + dark)
    print("  Last presence change: " + lastupdated)
    # get current time
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    # save to csv file
    with open('light_file.csv', 'a', newline = '') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow([current_time, lightlevel])


def knopjes():
    knop = "1"
    print("getting afstandsbediening " + str(knop) + " info")
    url = base + "sensors/2"
    r = requests.get(url)
    press = ""
    # format json
    rjson = r.json()
    name = str(rjson["name"])
    buttonevent = str(rjson["state"]["buttonevent"])
    if buttonevent.startswith("1"):
        press = "on"
    if buttonevent.startswith("2"):
        press = "up"
    if buttonevent.startswith("3"):
        press = "down"
    if buttonevent.startswith("4"):
        press = "off"
    lastupdated = str(rjson["state"]["lastupdated"])
    # print sensor info
    print("Afstandsbediening " + str(knop) + ":")
    print("  Name: " + name)
    print("  buttonevent: " + buttonevent)
    print("  press: " + press)
    print("  Last press change: " + lastupdated)


# turn on/off
def togglelight(lamp, boolean):
    # form url
    url = base + "lights/" + str(lamp) + "/state"
    # form body
    body = '{"on":' + str(boolean) + '}'
    r = requests.put(url, body)
    # format response
    rjson = r.json()
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
    # form url
    url = base + "lights/" + str(lamp) + "/state"
    # form body
    body = '{"bri":' + str(brightness) + '}'
    r = requests.put(url, body)
    # format response
    rjson = r.json()
    # filter response
    response = rjson[0]["success"]
    for k, v in response.items():
        # filter lamp no
        lamp = k.replace("/lights/", "").replace("/state/bri", "")
        # print result
        print("lamp " + lamp + " brightness is now " + str(v))


# zet kleur
def setcolor(lamp, color):
    # print("setting lamp 1 hue to " + str(color))
    # format request
    url = base + "lights/" + str(lamp) + "/state"
    body = '{"hue":' + str(color) + '}'
    r = requests.put(url, body)
    # format response
    rjson = r.json()
    response = rjson[0]["success"]
    # light = rjson["lights"][1]
    for k, v in response.items():
        # filter lamp no
        lamp = k.replace("/lights/", "").replace("/state/hue", "")
        # print result
        print("lamp " + lamp + " hue is now " + str(v))


# cycle colors
def colorcycle():
    # set delay
    delay = 1
    # set color interval
    interval = 6000
    i = 0
    for x in range(0, 65000):
        i = i + interval
        if i >= 65535:  # if i above max value, dont
            i = 0
        setcolor(1, i)
        time.sleep(delay)


# main script
if __name__ == '__main__':
    print('LHue starting')
    # create config
    checkconfig()
    # load config
    loadconfig()
    # continue huts
    checkonline()
    print('LHue ready')

    # while True:
    getmotionsensor()
    getambientlightsensor()
    # time.sleep(2)

    # knopjes()
    # get all lamp info
    # getlampinfo(1)
    # lamp aan
    # togglelight(1, "false")
    # zet brightness
    # setbrightness(1, 254)
    # zet kleur
    # setcolor(1, 00)
    # colorcycle()
    # while True:
        # getambientlightsensor()
        # time.sleep(5)
