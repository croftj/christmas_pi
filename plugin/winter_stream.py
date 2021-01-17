from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys
import math
import time

WHITE = Color(150, 150, 150)
COLOR_WHEEL = [BLUE, WHITE, CYAN, MAGENTA]

FORWARD = 0
BACKWARD = 1

def clamp(val, v_min, v_max):
#    print(f"val: {val}, min: {v_min}, max: {v_max}")
    return(max(min(v_max, val), v_min))

def load_plugin(update_lamps, num_lamps, lamps):
    return WinterStream(update_lamps, num_lamps, lamps)

class WinterStream(object):
    def __init__(self, update_lamps, num_lamps, lamps):
        # mandatory variables
        self.num_lamps = num_lamps
        self.update_lamps = update_lamps
        self.m_interval = .2      # Interval to be called in milliseconds
        self.strip_len = 5
        self.direction = BACKWARD
        self.direction = FORWARD
        self.cur_count = self.strip_len
        self.lamp_color = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))]


        # custom initialization
        self.increments = []
        self.states = []
        self.colors = []
        self.brightness = 100
        self.last_time = time.time()
        self.state = True
        self.cur_count = 0
        print("num_lamps = {}".format(num_lamps))

    def setBrightness(self, brightness):
        self.brightness = brightness

    def interval(self):
        return(self.m_interval)

    def setInterval(self, val):
        self.m_interval = val

    def init(self, lamps):
        if self.direction == FORWARD:
            self.direction = BACKWARD
        else:
            self.direction = FORWARD
        self.cur_count = self.strip_len
        self.lamp_color = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))]
        return

    def change(self, lamps):
        for ofs in range(0, self.num_lamps):
            if self.direction == FORWARD:
                lamp_ofs = self.num_lamps - 1 - ofs
                lamp_incr = -1
                lamp_end = 0
            else:
                lamp_ofs = ofs
                lamp_incr = 1
                lamp_end = self.num_lamps - 1
#            print(f"lamp_ofs = {lamp_ofs}")
#            if lamp_ofs != self.num_lamps - 1:
            if lamp_ofs > 0 and lamp_ofs < self.num_lamps - 1:
                lamps.colors[lamp_ofs] = lamps.colors[lamp_ofs + lamp_incr]
            if lamp_ofs == lamp_end:
                lamps.colors[lamp_ofs] = self.lamp_color
#                print(f"lamp_color[{lamp_ofs}]: {lamps.colors[lamp_ofs].str()}")
                self.cur_count -= 1
#                print(f"self.cur_count = {self.cur_count}")
                if self.cur_count <= 0:
                    self.cur_count = self.strip_len
                    lc = self.lamp_color
                    while lc == self.lamp_color:
                        lc = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))]
                    self.lamp_color = lc
#                    print(f"new lamp_color: { self.lamp_color}")
        self.update_lamps(lamps)
