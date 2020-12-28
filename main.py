# LHue main
# imports
import configparser
import sys

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
        config['HUEBRIDGE'] = {'ip' : '', 'key' : ''}
        # write to config
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        # config created
        print("Config created! stopping...")
        sys.exit(0)
    # config exists
    print("Config exists. continueing...")
    config = configparser.ConfigParser()
    config.read("config.ini")
    huebridge = config['HUEBRIDGE']
    if "ip" not in config["HUEBRIDGE"]:
        print("huts")





# main script
if __name__ == '__main__':
    print('LHue starting')
    # create config
    createconfig()
