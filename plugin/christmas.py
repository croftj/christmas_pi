from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys
import time

COLOR1 = Color(0, 0, 0)
COLOR2 = Color(0, 0, 0)
COLOR1 = Color(180, 80, 0)
COLOR2 = Color(180, 150, 0)
TWINKLE = Color(180, 0, 0)
#TWINKLE = YELLOW
TURNOVER = 1
TWINKLE_TIME = 6
TWINKLE_TIME = 12
COLOR1 = RED
COLOR2 = GREEN
TWINKLE = YELLOW
COLOR_WHEEL = [RED, GREEN, MAGENTA, Color(0, 0, 255), YELLOW]
NUM_COLORS = len(COLOR_WHEEL)

def load_plugin(update_lamps, num_lamps, lamps):
    return Christmas(update_lamps, num_lamps, lamps)

class Christmas(object):
    def __init__(self, update_lamps, num_lamps, lamps):
        # mandatory variables
        self.num_lamps = num_lamps
        self.update_lamps = update_lamps
        self.t_interval = .01      # Interval to be called in seconds
        self.change_time = 9000
        self.time_count = self.change_time
        self.cur_pattern = 0

        # custom initialization
        self.increments = []
        self.states = []
        self.colors = []
        self.fixedcolors = []
        self.on_times = []
        self.brightness = 100
        self.last_time = time.time()
        self.cur_color = COLOR1

#        print("num_lamps = {}".format(num_lamps))
        for i in range(0, num_lamps):
#            print("ia = {}".format(i))
            lamps.colors[i] = self.cur_color
        
#        print("num_lamps = {}".format(num_lamps))
        for i in range(0, num_lamps):
            nc = COLOR_WHEEL[random.randrange(0, NUM_COLORS)]
            while i > 0 and nc == self.fixedcolors[i-1]:
                nc = COLOR_WHEEL[random.randrange(0, NUM_COLORS)]

            self.fixedcolors.append(nc)
            self.increments.append(random.randrange(20, 427))
            self.on_times.append(random.randrange(300, 1500))
            lamps.colors[i] = self.fixedcolors[i]
#            print("ib = {}, Color({})".format(i, self.fixedcolors[i].str()))
        
    def setBrightness(self, brightness):
        self.brightness = brightness

    def interval(self):
        return(self.t_interval)

    def setInterval(self, val):
        self.t_interval = val

    def init(self, lamps):
        return

    def change(self, lamps):
        haveChange = False
        if self.cur_pattern == 0:
            for i in range(0, self.num_lamps):
                self.increments[i] -= 1
                if self.increments[i] <= 0:
                    haveChange = True
                    if lamps.colors[i].equals(self.fixedcolors[i]):
    #                        print("off: ib = {}".format(i))
                        lamps.colors[i] = BLACK
                        self.increments[i] = random.randrange(30, 400)
    #                        print("inc[{}] = {}".format(i, self.increments[i]))
                    else:
    #                        print("on: ib = {}".format(i))
                        lamps.colors[i] = self.fixedcolors[i]
                        self.increments[i] = self.on_times[i]
    #                        print("FLASH[{}] = {}, Color({})".format(i, self.increments[i], self.fixedcolors[i].str()))

        if haveChange:
            self.update_lamps(lamps)
        

