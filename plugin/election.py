from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys
import math
import time

COLOR1 = Color(0, 0, 0)
COLOR2 = Color(0, 0, 0)
COLOR1 = Color(180, 80, 0)
COLOR2 = Color(180, 150, 0)
TWINKLE = Color(180, 0, 0)
#TWINKLE = YELLOW
TURNOVER = 1
TWINKLE_TIME = 6
TWINKLE_TIME = 9
SPACING = 2

ON_COUNT = 3
OFF_COUNT = 2

def clamp(val, v_min, v_max):
#    print(f"val: {val}, min: {v_min}, max: {v_max}")
    return(max(min(v_max, val), v_min))

def load_plugin(update_lamps, num_lamps, lamps):
    return Election(update_lamps, num_lamps, lamps)

class Election(object):
    def __init__(self, update_lamps, num_lamps, lamps):
        # mandatory variables
        self.num_lamps = num_lamps
        self.update_lamps = update_lamps
        self.m_interval = .2      # Interval to be called in milliseconds

        # custom initialization
        self.increments = []
        self.states = []
        self.colors = []
        self.brightness = 100
        self.last_time = time.time()
        self.cur_color = COLOR1
        self.state = True
        self.on_cnt = SPACING
        self.midpoint = int(self.num_lamps / 2)
        self.battle_cnt = 60
        self.start_cnt = 0
        self.black_cnt = 0
        self.explosion = 0
        print("num_lamps = {}".format(num_lamps))

    def setBrightness(self, brightness):
        self.brightness = brightness

    def interval(self):
        return(self.m_interval)

    def setInterval(self, val):
        self.m_interval = val

    def init(self, lamps):
        return

    def change(self, lamps):
#        print("here")
        haveChange = False
        if True:
            self.battle_cnt -= 1
            if self.battle_cnt == 0:
                self.battle_cnt = random.randrange(30, 90)
                dir = random.randrange(1, 100)
                if dir > 50:
                    self.midpoint = clamp(self.midpoint + random.randrange(0, +7), 20, self.num_lamps - 20)
                else:
                    self.midpoint =  clamp(self.midpoint - random.randrange(0, +7), 20, self.num_lamps - 20)
                print(f"battle_cnt = {self.battle_cnt}, midpoint = {self.midpoint}")
            i = self.midpoint
            n = 0
            s_cnt = self.start_cnt
            b_cnt = self.black_cnt
            for n in range(0, self.num_lamps):
                i = n
                j = self.num_lamps - 1 - n
#                print(f"n: {n}, i: {i}, j: {j}")
                if i > self.midpoint:
                    if s_cnt < ON_COUNT:
                        lamps.colors[i] = RED
                    elif b_cnt < OFF_COUNT:
                        lamps.colors[i] = BLACK

                if j < self.midpoint:
                    if s_cnt < ON_COUNT:
                        lamps.colors[j] = BLUE
                    elif b_cnt < OFF_COUNT:
                        lamps.colors[j] = BLACK

                if s_cnt == ON_COUNT and b_cnt == OFF_COUNT:
                    s_cnt = 0
                    b_cnt = 0
                elif s_cnt < ON_COUNT:
                    s_cnt += 1
                elif b_cnt < OFF_COUNT:
                    b_cnt += 1

            if self.start_cnt == ON_COUNT and self.black_cnt == OFF_COUNT:
                self.start_cnt = 0
                self.black_cnt = 0
            elif self.start_cnt < ON_COUNT:
                self.start_cnt += 1
            elif self.black_cnt < OFF_COUNT:
                self.black_cnt += 1

            if self.explosion == 0:
                self.explosion = random.randrange(5, 12)
#                print(f"explosion = {self.explosion}")
            for n in range(0, self.explosion): # range(1, 12):
                i = clamp(self.midpoint - n, 0, self.num_lamps)
                j = clamp(self.midpoint + n, 0, self.num_lamps - 1)
                if n == 1:
                    lamps.colors[i] = Color(255, 255, 255)
                    lamps.colors[j] = Color(255, 255, 255)
                else:
                    t = 3
                    e = int(random.random() * 4*math.cos(math.radians(n))+1)
#                    print(f"exp = {self.explosion}, n = {n}, e = {e}{'*' if e < t else ''}")
                    if e < t:
                        lamps.colors[i] = Color(255, 255, 255)
                        lamps.colors[j] = Color(255, 255, 255)
#            lamps.colors[self.midpoint] = Color(255, 255, 255)
            self.explosion -= 1
#            print("\n")

        self.update_lamps(lamps)

        

