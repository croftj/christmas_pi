#!/usr/bin/python3
##########################################################
# This program will control NeoPixel LED lamps which are #
# connected to a Wifi Pixel controller.                  #
##########################################################

from find_plugins import find

import time
import importlib
import os
import random
import re
import sacn
import sys
import time

from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray

NUM_LAMPS = 100
TIME_RANGE_REG = re.compile("(\d\d):(\d\d)-(\d\d):(\d\d)")
COLOR_WHEEL = [RED, GREEN, BLUE, YELLOW, MAGENTA]

brightness = 100
sender = sacn.sACNsender()

patterns        = ''
runtime         = 300 * 60
brightness      = 100
ipaddr          = "universe1"
start_time      = ""
end_time        = ""
pattern_interval = 240
NUM_LAMPS       = 200
cfn             = ""
on_times        = None

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

############################################################
# Callback function used by the plugins to update the LEDs #
# when needed.                                             #
############################################################
def update_lamps(data):
    sender[1].dmx_data = data.as_list(brightness)

#############################################################
# Parses the array of time ranges in the format of          #
# "hh:mm-hh:mm" into begining and ending times expressed    #
# as minutes relative to start of the day.  The time ranges #
# may wrap around midnight (00:00)                          #
#############################################################
def set_times(ranges):
    global on_times
    on_times = []
    for trange in ranges:
        begin, end = trange.split("-")
        hr, min = begin.split(":")
        bt = int(hr) * 60 + int(min)
        hr, min = end.split(":")
        et = int(hr) * 60 + int(min)
        on_times.append((bt, et))

#############################################
# Parse the array of configuration options. #
#############################################
def parse_options(args):
    global brightness
    global patterns
    global runtime
    global brightness
    global ipaddr
    global start_time
    global end_time
    global pattern_interval
    global NUM_LAMPS
    global cfn
    for arg in args:
        if len(arg.split('=')) > 1:
            (cmd, val) = arg.split('=', 2)
            print(f"cmd = {cmd}, val = {val}")
            if len(val) > 0:
                if "brightness" in cmd.lower():
                    brightness = int(val)
                if "interval" in cmd.lower():
                    pattern_interval = int(val) # * 60
                if "pattern" in cmd.lower():
                    print(f"Have pattern option: {val}")
                    patterns = val
                    print(f"patterns: {patterns}")
                if "numlamps" in cmd.lower():
                    NUM_LAMPS = int(val)
                if "dir" in cmd.lower():
                    os.chdir(val)
                if "config" in cmd.lower():
                    cfn = val
                if "ipaddr" in cmd.lower():
                    ipaddr = val
                if "start" in cmd.lower():
                    start_time = val
                if "end" in cmd.lower():
                    end_time = val
                if "on_times" in cmd.lower():
                    ranges = val.split(",")
                    set_times(ranges)

############################################################
# Returns True is time falls within the time range defined #
# in time_range.                                           #
############################################################
def test_time(time_range, time):
    if time_range[0] <= time_range[1]:
        if time >= time_range[0] and time < time_range[1]:
            return True
    else:
        if time >= time_range[0] or time < time_range[1]:
            return True
    return False

if __name__ == "__main__":
    sys.stdout = Unbuffered(sys.stdout)
    runtime = 4 * 60 * 60
    interval = 0
    
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
    
    sender.start()                          # start the sending thread
    sender.activate_output(1)               # start sending out data in the 1st universe
    sender[1].multicast = False             # set multicast to False
    sender[1].destination = ipaddr          # provide the destination address

    print(f"NUM_LAMPS = {NUM_LAMPS}")
    data = ColorArray(NUM_LAMPS, RED)

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
    if len(pattern_list) == 1:
        pattern_interval = 0
    
    random.seed(time)

    color_ofs = 0
    pattern = pattern_list[0]

    pattern.setBrightness(brightness)

    print("interval = {}".format(interval))
    
    if len(cfn) > 0:
        cfn_modtime = os.stat(cfn).st_mtime
    last_time = time.time()
    last_pattern_time = time.time()
    power_on = True
    print("Starting loop!")
    while True:
        if len(cfn) > 0:
            if os.stat(cfn).st_mtime > cfn_modtime:
                for i in range(0, NUM_LAMPS):
                    data.colors[i] = BLACK
                sys.exit(1)
        
        now = time.localtime()
#        print(f"now = {now}")
        minutes = now.tm_hour * 60 + now.tm_min
#        print(f"mins = {minutes}")
        power_on = False
        for time_range in on_times:
#            print(f"time_range = {time_range}")
            power_on = test_time(time_range, minutes)
#            print(f"power_on = {power_on}")
            if power_on:
                break

        if power_on:
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
#            print("Calling patther.change()")
                pattern.change(data)
            time.sleep(interval / 2)
        else:
            for i in range(0, NUM_LAMPS):
                data.colors[i] = BLACK
            update_lamps(data)

    print("Stopping sender in 5")
    time.sleep(5)
    sender.stop()


        
                    


