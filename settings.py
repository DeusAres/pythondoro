import configparser
from pathlib import Path


def first():
    config = configparser.RawConfigParser()

    config.add_section('Timer')
    def configSet(a, b):
        config.set('Timer', a, b)

    configSet('pomodoro','45')
    configSet('pause', '5')
    configSet('autopomodoro', 'true')
    configSet('autopause', 'true')

    path = str(Path(__file__).parents[0] / "settings.cfg")
    with open(path, 'w') as configfile:
        config.write(configfile)

def read():
    config = configparser.RawConfigParser()
    config.read(str(Path(__file__).parents[0] / "settings.cfg"))

    sets = {}
    def getInt(a):
        sets[a] = config.getint('Timer', a)
    def getBoolean(a):
        sets[a] = config.getboolean('Timer', a)

    [getInt(each) for each in ['pomodoro', 'pause']]
    [getBoolean(each) for each in ['autopomodoro', 'autopause']]

    return sets

def set(values):
    config = configparser.RawConfigParser()
    config.add_section('Timer')

    def configSet(a):
        config.set('Timer', a, values[a])

    [configSet(each) for each in ['pomodoro', 'pause', 'autopomodoro', 'autopause']]

    path = str(Path(__file__).parents[0] / "settings.cfg")
    with open(path, 'w') as configfile:
        config.write(configfile)

