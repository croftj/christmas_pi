from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys
import time

COLOR1 = Color(0, 0, 0)
COLOR2 = Color(0, 0, 0)
COLOR1 = Color(0, 0, 150)
COLOR2 = Color(0, 0, 150)
#COLOR2 = Color(120, 120, 220)
TWINKLE = Color(255, 255, 255)
#TWINKLE = YELLOW
TURNOVER = 1
TWINKLE_TIME = 6
TWINKLE_TIME = 9

def load_plugin(update_lamps, num_lamps, lamps):
    return Christmas(update_lamps, num_lamps, lamps)

class Christmas(object):
    def __init__(self, update_lamps, num_lamps, lamps):
        # mandatory variables
        self.num_lamps = num_lamps
        self.update_lamps = update_lamps
        self.m_interval = .01      # Interval to be called in milliseconds

        # custom initialization
        self.increments = []
        self.states = []
        self.colors = []
        self.brightness = 100
        self.last_time = time.time()
        self.cur_color = COLOR1

        print("num_lamps = {}".format(num_lamps))
        for i in range(0, num_lamps):
            print("i = {}".format(i))
            lamps.colors[i] = self.cur_color
            self.increments.append(random.randrange(20, 427))
        
    def setBrightness(self, brightness):
        self.brightness = brightness

    def interval(self):
        return(self.m_interval)

    def setInterval(self, val):
        self.m_interval = val

    def init(self, lamps):
        return

    def change(self, lamps):
        haveChange = False
        if time.time() > self.last_time + TURNOVER:
            self.last_time = time.time()
            if self.cur_color.equals(COLOR1):
                self.cur_color = COLOR2
            else:
                self.cur_color = COLOR1

        for i in range(0, self.num_lamps):
            self.increments[i] -= 1
            if self.increments[i] <= 0:
                haveChange = True
                if lamps.colors[i].equals(TWINKLE):
                    lamps.colors[i] = self.cur_color
                    self.increments[i] = random.randrange(10, 200)
#                    print("inc[{}] = {}".format(i, self.increments[i]))
                else:
                    lamps.colors[i] = TWINKLE
                    self.increments[i] = TWINKLE_TIME
#                    print("FLASH[{}] = {}".format(i, self.increments[i]))

        if haveChange:
            self.update_lamps(lamps)

        

