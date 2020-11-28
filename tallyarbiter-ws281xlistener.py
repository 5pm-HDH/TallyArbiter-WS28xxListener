## Tally Arbiter Python Listener

from signal import signal, SIGINT
from sys import exit
import sys
import time
from rpi_ws281x import PixelStrip, Color
import socketio
import json

device_states = []
bus_options = []
mode_preview = False
mode_program = False

if len(sys.argv) > 1:
    configFileName = sys.argv[1]
else:
    configFileName = 'config_ws281x.json'

server_config = {}
led_config = {}

# SocketIO Connections
sio = socketio.Client()


@sio.event
def connect():
    print('Connected to Tally Arbiter server:', server_config["ip"], server_config["port"])
    sio.emit('bus_options')  # get current bus options
    sio.emit('device_listen_blink', {'deviceId': led_config["deviceId"]})  # start listening for the device
    repeatNumber = 2
    while (repeatNumber):
        repeatNumber = repeatNumber - 1
        doBlink(0, 255, 0)
        time.sleep(.3)
        doBlink(0, 0, 0)
        time.sleep(.3)


@sio.event
def connect_error(data):
    print('Unable to connect to Tally Arbiter server:', server_config["ip"], server_config["port"])
    doBlink(150, 150, 150)
    time.sleep(.3)
    doBlink(0, 0, 0)
    time.sleep(.3)


@sio.event
def disconnect():
    print('Disconnected from Tally Arbiter server:', server_config["ip"], server_config["port"])
    doBlink(255, 255, 255)
    time.sleep(.3)
    doBlink(0, 0, 0)
    time.sleep(.3)


@sio.event
def reconnect():
    print('Reconnected to Tally Arbiter server:', server_config["ip"], server_config["port"])
    repeatNumber = 2
    while (repeatNumber):
        repeatNumber = repeatNumber - 1
        doBlink(0, 255, 0)
        time.sleep(.3)
        doBlink(0, 0, 0)
        time.sleep(.3)


@sio.on('device_states')
def on_device_states(data):
    global device_states
    device_states = data
    processTallyData()


@sio.on('bus_options')
def on_bus_options(data):
    global bus_options
    bus_options = data


@sio.on('flash')
def on_flash():
    doBlink(255, 255, 255)
    time.sleep(.5)
    doBlink(0, 0, 0)
    time.sleep(.5)
    doBlink(255, 255, 255)
    time.sleep(.5)
    doBlink(0, 0, 0)
    time.sleep(.5)
    doBlink(255, 255, 255)
    time.sleep(.5)
    evaluateMode()


@sio.on('reassign')
def on_reassign(oldDeviceId, newDeviceId):
    print('Reassigning from DeviceID: ' + oldDeviceId + ' to Device ID: ' + newDeviceId)
    doBlink(0, 0, 0)
    time.sleep(.1)
    doBlink(0, 0, 255)
    time.sleep(.1)
    doBlink(0, 0, 0)
    time.sleep(.1)
    doBlink(0, 0, 255)
    time.sleep(.1)
    doBlink(0, 0, 0)
    sio.emit('listener_reassign', data=(oldDeviceId, newDeviceId))

    led_config["deviceId"] = newDeviceId
    config_file = open(configFileName, 'w')
    configJson = {}
    configJson['server_config'] = server_config
    configJson['led_config'] = led_config
    config_file.write(json.dumps(configJson, indent=4))
    config_file.close()


def getBusTypeById(busId):
    for bus in bus_options:
        if bus['id'] == busId:
            return bus['type']


def processTallyData():
    global mode_preview
    global mode_program
    for device_state in device_states:
        if getBusTypeById(device_state['busId']) == 'preview':
            if len(device_state['sources']) > 0:
                mode_preview = True
            else:
                mode_preview = False
        elif getBusTypeById(device_state['busId']) == 'program':
            if len(device_state['sources']) > 0:
                mode_program = True
            else:
                mode_program = False
    evaluateMode()


def evaluateMode():
    if (mode_preview == True) and (mode_program == False):  # preview mode, color it green
        doBlink(0, 255, 0)
    elif (mode_preview == False) and (mode_program == True):  # program mode, color it red
        doBlink(255, 0, 0)
    elif (mode_preview == True) and (mode_program == True):  # preview+program mode, color it yellow
        doBlink(255, 127, 0)
    else:  # no source, turn it off
        doBlink(0, 0, 0)


def doBlink(r, g, b):
    color = Color(r, g, b)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(100.0 / 1000.0)


try:
    config_file = open(configFileName)
    config = config_file.read()
    config_file.close()
    if config != '':
        configJson = json.loads(config)
        server_config = configJson['server_config']
        led_config = configJson['led_config']
    else:
        print('Config data could not be loaded.')
        exit(0)
except IOError:
    print('Config file could not be located.')
    exit(0)

# Intialize the library (must be called once before other functions).
strip = PixelStrip(led_config["LED_COUNT"], led_config["LED_PIN"], led_config["LED_FREQ_HZ"], led_config["LED_DMA"],
                   led_config["LED_INVERT"], led_config["LED_BRIGHTNESS"], led_config["LED_CHANNEL"])
strip.begin()

while 1:
    try:
        sio.connect('http://' + server_config["ip"] + ':' + str(server_config["port"]))
        sio.wait()
        print('Tally Arbiter Listener Running. Press CTRL-C to exit.')
        print(
            'Attempting to connect to Tally Arbiter server: ' + server_config["ip"] + '(' + str(server_config["port"]) + ')')
    except KeyboardInterrupt:
        print('Exiting Tally Arbiter Listener.')
        doBlink(0, 0, 0)
        exit(0)
    except socketio.exceptions.ConnectionError:
        doBlink(0, 0, 0)
        time.sleep(15)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print('An error occurred internally.')
        doBlink(0, 0, 0)
