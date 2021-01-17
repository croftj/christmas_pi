from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys
import time

COLOR_WHEEL = [RED, CYAN, GREEN, MAGENTA, BLUE, YELLOW]
#COLOR_WHEEL = [
#                Color(255, 150, 150)
#              , Color(100, 255, 255)
#              , Color(150, 255, 150)
#              , Color(250, 150, 255)
#              , Color(120, 120, 255)
#              , Color(255, 255, 80)
#            ]

TURNOVER = 300
#TURNOVER = 20

def load_plugin(update_lamps, num_lamps, lamps):
    return Traverse(update_lamps, num_lamps, lamps)

class Traverse(object):
    def __init__(self, update_lamps, num_lamps, lamps):
        # mandatory variables
        self.num_lamps = num_lamps
        self.update_lamps = update_lamps
        self.m_interval = .03      # Interval to be called in milliseconds

        # custom initialization
        self.increments = []
        self.states = []
        self.colors = []
        self.brightness = 100
        self.last_time = time.time()
        self.in_transition = False
        self.cur_color = random.randrange(0, len(COLOR_WHEEL))
        self.last_color = self.cur_color
        print("num_lamps = {}".format(num_lamps))
        for color in COLOR_WHEEL:
            self.increments.append(1)
        for i in range(0, num_lamps):
                    return haveChange

    def setBrightness(self, brightness):
        self.brightness = brightness

    def interval(self):
        return(self.m_interval)

    def setInterval(self, val):
        self.m_interval = val

    def clr_lamps(self, lamp, color, lamps):
        state = 0
        lamp1 = self.start_lamp - lamp
        lamp2 = self.start_lamp + lamp
        if lamp1 >= self.max_lamp:
            lamps.colors[lamp1] = COLOR_WHEEL[color]
        if lamp2 < self.num_lamps - self.max_lamp:
            lamps.colors[lamp2] = COLOR_WHEEL[color]
        print("clr num_lamps = {}, lamp1 = {}, lamp2 = {}".format(self.num_lamps, lamp1, lamp2))

    def set_lamps(self, lamp, color, lamps):
        state = 0
        lamp1 = self.start_lamp - lamp
        lamp2 = self.start_lamp + lamp

        print("color 0 = {}".format(COLOR_WHEEL[color].str()))
        if lamp1 >= 0 and not lamps.colors[lamp1].equals(COLOR_WHEEL[color]):
            print("color 1 = {}".format(lamps.colors[lamp1].str()))
            state += 1
            lamps.colors[lamp1] = COLOR_WHEEL[color]
        if lamp2 < self.num_lamps and not lamps.colors[lamp2].equals(COLOR_WHEEL[color]):
            print("color 2 = {}".format(lamps.colors[lamp2].str()))
            state += 1
            lamps.colors[lamp2] = COLOR_WHEEL[color]
        print("set num_lamps = {}, lamp1 = {}, lamp2 = {}, state = {}".format(self.num_lamps, lamp1, lamp2, state))
        return(state == 0)   

    def init(self, lamps):
        return

    def change(self, lamps):
        haveChange = False
        if not self.in_transition and time.time() > self.last_time + TURNOVER:
            self.cur_color = (self.last_color + self.increments[self.last_color]) % len(COLOR_WHEEL)
            inc = self.increments[self.last_color] + 1
            if inc >= len(COLOR_WHEEL):
                inc = 1
            self.increments[self.last_color] = inc
    #        print("color = {}, increment[{}] = {}".format(color, self.last_color, self.increments[self.last_color]))
            print("color = {}, increment[{}] = {}: {}".format(self.cur_color, self.last_color, self.increments[self.last_color], COLOR_WHEEL[self.cur_color].str()))
            haveChange = True
            self.in_transition = True
            self.start_lamp = random.randrange(int(self.num_lamps / 6), int(self.num_lamps / 6) * 5)
            self.cur_lamp = 0
            self.lamp = 0

        if self.in_transition:
            lamps.colors[self.cur_lamp] = COLOR_WHEEL[self.cur_color]
            lamps.colors[self.num_lamps - self.cur_lamp - 1] = COLOR_WHEEL[self.cur_color]
            self.cur_lamp += 1
            count = 0
            for i in range(0, self.num_lamps):
#                print("color i = {}".format(lamps.colors[i].str()))
                if lamps.colors[i].equals(COLOR_WHEEL[self.cur_color]):
                    count += 1
            print("test count = {}".format(count))
            if count > self.num_lamps - 2:
                self.last_color = self.cur_color
                self.in_transition = False
                self.last_time = time.time()
            haveChange = True
        if haveChange:
            self.update_lamps(lamps)

        

