#!/usr/bin/python3
###############################################################
# This program will control NeoPixel LED dispays  which are   #
# directly connected to a GPIO pin of a Rasberry PI. It also, #
# polls a switch to determine if the lights should be on or   #
# off without removing power from neither the Raspberry PI    #
# not the lamps                                               #
###############################################################

from find_plugins import find

import board
from digitalio import DigitalInOut, Direction, Pull
from SuperNeoPixel import SuperNeoPixel
from button import Button, ButtonState
import board
import importlib
import neopixel
import numpy as np
import os
import random
import sys
import time

from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray

# LED strip configuration:
LED_PIN         = board.D18     # Gpio pin connected to the NeoPixel Lamps
PWR_BUTTON      = board.D24     # Gpio pin connected to the power button
CYC_BUTTON      = board.D25     # Gpio pin for moving to the next sequence (not implimented)
LED_ORDER       = neopixel.RGB  # order of LED colours. May also be RGB, GRBW, or RGBW
LED_BRIGHTNESS  = 1.0
# Create NeoPixel object with appropriate configuration.

NUM_LAMPS = 100

COLOR_WHEEL = [RED, GREEN, BLUE, YELLOW, MAGENTA]

brightness = 100
lamps = None
patterns = ''
runtime = 300 * 60
brightness = 100
pattern_interval = 240
NUM_LAMPS = 200
cfn = ""

def ChangeColor(color, data, brightness):
    while not data.colors[0].equals(color):
#        print("cur: {}, tgt: {}".format(data.colors[0].str(), color.str()))
        for i in range(0, NUM_LAMPS):
            data.colors[i] = data.colors[i].step_to(color, 1)
        colors = data.as_list(brightness)
        strip.set_array(colors)
        time.sleep(.06)

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def test_switch(switch):
    rv = 0
    cnt1 = 3
    while cnt1 > 0 and rv == 0:
        cnt1 -= 1
        if not switch.value:
            time.sleep(0.01)
            if not switch.value:
                while not switch.value:
                    rv += 1
                    time.sleep(.02)
    return rv

############################################################
# Callback function used by the plugins to update the LEDs #
# when needed.                                             #
############################################################
def update_lamps(data):
    lamps.set_array(data.colors, brightness)
    lamps.show()

#############################################
# Parse the array of configuration options. #
#############################################
def parse_options(args):
    global brightness
    global lamps
    global patterns
    global runtime
    global brightness
    global pattern_interval
    global NUM_LAMPS
    global cfn
    for arg in args:
        if len(arg.split('=')) > 1:
            (cmd, val) = arg.split('=', 2)
            if len(val) > 0:
                if "runtime" in cmd.lower():
                    runtime = int(val) * 60
                if "brightness" in cmd.lower():
                    brightness = int(val)
                if "interval" in cmd.lower():
                    pattern_interval = int(val) # * 60
                if "pattern" in cmd.lower():
                    patterns = val
                if "numlamps" in cmd.lower():
                    NUM_LAMPS = int(val)
                if "dir" in cmd.lower():
                    os.chdir(val)
                if "config" in cmd.lower():
                    cfn = val


if __name__ == "__main__":
    sys.stdout = Unbuffered(sys.stdout)
    runtime = 4 * 60 * 60
    interval = 0
    
    power_btn = Button(PWR_BUTTON, 80, 200)
    cycle_btn = Button(CYC_BUTTON, 80, 200)

    #########################################################
    # Get the options from the command line. The sole       #
    # purpose of initial call to parse_options is to get    #
    # the name of the configuration file if provided. If it #
    # is present, it wll be parsed first then followed by   #
    # parsing the command line aguments a second so that    #
    # any command line options will take precedence over    #
    # the configuration options.                            #
    #########################################################
    args = sys.argv[1:]
    parse_options(args)
    if len(cfn) > 0:
        args = []
        for arg in open(cfn, 'r'):
            print(f"have arg: {arg}")
            arg = arg.strip()
            args.append(arg)
        parse_options(args)

    ##########################################################
    # Create and initialize the array of NeoPixel lamps that #
    # will be controlled.                                    #
    ##########################################################
    print(f"NUM_LAMPS = {NUM_LAMPS}")
    lamps = SuperNeoPixel(LED_PIN, NUM_LAMPS, brightness = LED_BRIGHTNESS, auto_write=False, pixel_order = LED_ORDER)
    data = ColorArray(NUM_LAMPS, RED)
    lamps.set_array(data.colors, brightness)

    #########################################################
    # Find the plugins and populate the array of plugins to #
    # sequence through. Order the plugins in the same order #
    # as they are defined in the pattern= option            #
    #########################################################
    print(f"patterns = {patterns}")
    pn_names = patterns.split(",");
    pattern_list = []
    modules = {}
    plugins = find("plugin")
    print(f"pn_names = {pn_names}")
    print(f"plugins = {plugins}")
    for mod_name in plugins:
        print(f"Adding module: {mod_name}")
        mod = importlib.import_module(plugins[mod_name])
        modules[mod_name] = mod
    for plugin in pn_names:
        print(f"Adding plugin: {plugin}")
        module = modules[plugin].load_plugin(update_lamps, NUM_LAMPS, data)
        pattern_list.append(module)

    pattern_ofs = 0
    ####################################################
    # If there is only one pattern, there should be no #
    # interval for sequencing through them.            #
    ####################################################
    if len(pattern_list) == 1:
        pattern_interval = 0
    
    random.seed(time)

    ##################
    # Light the fuse #
    ##################
    lamps.show()

    color_ofs = 0
    pattern = pattern_list[0]

    pattern.setBrightness(brightness)

    print("interval = {}".format(interval))
    lamps.set_array(data.colors, brightness)
    
    if len(cfn) > 0:
        cfn_modtime = os.stat(cfn).st_mtime
    last_time = time.time()
    last_pattern_time = time.time()
    power_on = True

    #########################
    # And let them shine!!! #
    #########################
    while True:
        if len(cfn) > 0:
            if os.stat(cfn).st_mtime > cfn_modtime:
                for i in range(0, NUM_LAMPS):
                    data.colors[i] = BLACK
                lamps.set_array(data.colors)
                lamps.show()
                sys.exit(1)

        pwr = power_btn.read()
        if pwr != None:
            print(f"pwr = {pwr}")
        cyc = cycle_btn.read()
        if pwr != None and pwr == ButtonState.SWITCH_ON:
            power_on = not power_on
        if power_on:
#            print(f"pattern_interval = {pattern_interval}, last_pattern_time = {last_pattern_time}")
            if pattern_interval > 0 and last_pattern_time < time.time() - pattern_interval:
                last_pattern_time = time.time()
                if pattern_ofs >= len(pattern_list):
                    pattern_ofs = 0
#                print(f"changing to pattern {pattern_ofs}")
                pattern = pattern_list[pattern_ofs]
                pattern_ofs += 1
                pattern.init(data)
                last_time = time.time() - pattern.interval() - 1

            if last_time < time.time() - pattern.interval():
                last_time = time.time()
                if pattern.change(data):
    #                print(f"Setting lamps! {data.colors}")
                    lamps.set_array(data.colors, brightness)
                    lamps.show()
            time.sleep(interval / 2)

        #######################################
        # Unless they are intended to be off! #
        #######################################
        else:
            for i in range(0, NUM_LAMPS):
                data.colors[i] = BLACK
            lamps.set_array(data.colors)
            lamps.show()
