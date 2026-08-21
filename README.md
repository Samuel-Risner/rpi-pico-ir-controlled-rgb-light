# rpi-pico-ir-controlled-rgb-light

RGB light controlled by a Raspberry Pi Pico via Infrared

# Setup

## 1. Install MicroPython on the Raspberry Pi Pico

## 2. Upload code

Upload this repositories `main.py` file

And some files from [Peter Hinch's](https://github.com/peterhinch) repository [micropython_ir](https://github.com/peterhinch/micropython_ir) to the folder `ir_nx`:

(You can also find the files in this repository under `micropython_ir`)

 - `ir_rx/init.py`
 - `ir_rx/nec.py`

The filesystem on the Raspberry Pi Pico should look like this after copying all three files:

```
main.py
ir_rx
    /init.py
    /nec.py
```

## 3. Modify code

### 3.1 Change the GPIO Pins to match your setup

```py
# GPIO Pins on the Raspberry Pi Pico
PIN_RED = 18
PIN_GREEN = 20
PIN_BLUE = 22
PIN_IR = 21
```

### 3.2 Change the colors and data/addr attributes (if required)

The colors are in the format `[red, green, blue]`

You can use the file `colors.js` to auto generate the colors from rgb values (`0-255`) instead of entering the frequencies (`0-65535`)

The `data` attribute is the part before the `-` and matches the remotes buttons

The `addr` attribute is the part after the `-` and matches the remote

```py
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
```

# License

This project is licensed under the GPL-3.0 license (see the file `LICENSE` for more information)

The folder `micropython_ir` is excluded from this license, since it is licensed by Peter Hinch under the MIT license

You can find his repository with the original code [here](https://github.com/peterhinch/micropython_ir) and a copy of the MIT license in the folder `micropython_ir` in the file `LICENSE`