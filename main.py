import time
from machine import Pin, PWM
from ir_rx.nec import NEC_16

# GPIO Pins on the Raspberry Pi Pico
PIN_RED = 18
PIN_GREEN = 20
PIN_BLUE = 22
PIN_IR = 21

PWM_FREQUENCY = 1000

MIN_BRIGHTNESS = 65535
MAX_BRIGHTNESS = 0

PWM_RED = PWM(Pin(PIN_RED))
PWM_GREEN = PWM(Pin(PIN_GREEN))
PWM_BLUE = PWM(Pin(PIN_BLUE))

PWM_RED.freq(PWM_FREQUENCY)
PWM_GREEN.freq(PWM_FREQUENCY)
PWM_BLUE.freq(PWM_FREQUENCY)

# initialize to white (step 1/2)
PWM_RED.duty_u16(MAX_BRIGHTNESS)
PWM_GREEN.duty_u16(MAX_BRIGHTNESS)
PWM_BLUE.duty_u16(MAX_BRIGHTNESS)

ACTIONS = {
    "00-ef00": ["brightness+", 0.01],
    "01-ef00": ["brightness-", 0.01],
    "02-ef00": ["off"],
    "03-ef00": ["on"],

    "04-ef00": [MAX_BRIGHTNESS, MIN_BRIGHTNESS, MIN_BRIGHTNESS], # red
    "05-ef00": [MIN_BRIGHTNESS, MAX_BRIGHTNESS, MIN_BRIGHTNESS], # green
    "06-ef00": [MIN_BRIGHTNESS, MIN_BRIGHTNESS, MAX_BRIGHTNESS], # blue
    "07-ef00": [MAX_BRIGHTNESS, MAX_BRIGHTNESS, MAX_BRIGHTNESS], # white

    "08-ef00": [0,52428,65535],
    "09-ef00": [62194,28270,54741],
    "0a-ef00": [61423,39321,13878],
    "0c-ef00": [0,28270,65535],
    "0d-ef00": [65535,0,0],
    "0e-ef00": [34181,57311,12593],
    "10-ef00": [0,17476,65535],
    "11-ef00": [60395,17476,14392],
    "12-ef00": [34952,56540,22359],
    "14-ef00": [6682,0,65535],
    "15-ef00": [57311,39064,38550],
    "16-ef00": [5397,65535,0],
}

brightness_rel = 1
MIN_BRIGHTNESS_REL = 0.01
MAX_BRIGHTNESS_REL = 1

# initialize to white (step 2/2)
red = MAX_BRIGHTNESS
green = MAX_BRIGHTNESS
blue = MAX_BRIGHTNESS

def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        # print('Repeat code.')
        return

    global brightness_rel
    global red
    global green
    global blue

    key = "{:02x}-{:04x}".format(data, addr)
    action = ACTIONS.get(key)

    if action is None:
        print("No action for {}".format(key))
        return

    print("Action: {}".format(action))

    # turn off
    if action[0] == "off":
        PWM_RED.duty_u16(MIN_BRIGHTNESS)
        PWM_GREEN.duty_u16(MIN_BRIGHTNESS)
        PWM_BLUE.duty_u16(MIN_BRIGHTNESS)
        return

    # brightness +
    elif action[0] == "brightness+":
        brightness_rel += action[1]
        if brightness_rel > MAX_BRIGHTNESS_REL:
            brightness_rel = MAX_BRIGHTNESS_REL

    # brightness -
    elif action[0] == "brightness-":
        brightness_rel -= action[1]
        if brightness_rel < MIN_BRIGHTNESS_REL:
            brightness_rel = MIN_BRIGHTNESS_REL

    # set RGB values
    else:
        if action[0] != "on":
            red = action[0]
            green = action[1]
            blue = action[2]

        # reset brightness if turned on again
        else:
            brightness_rel = MAX_BRIGHTNESS_REL
        
    PWM_RED.duty_u16(int(red * brightness_rel))
    PWM_GREEN.duty_u16(int(green * brightness_rel))
    PWM_BLUE.duty_u16(int(blue * brightness_rel))

ir = NEC_16(Pin(PIN_IR, Pin.IN), callback)

while True:
    time.sleep_ms(500)