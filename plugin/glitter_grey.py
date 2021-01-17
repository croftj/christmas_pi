from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys
import time

WHITE = Color(255, 210, 210)
COLOR_WHEEL = [RED, CYAN, GREEN, MAGENTA, Color(0, 0, 255), YELLOW, Color(200, 150,0)]
COLOR_WHEEL1 = [RED, GREEN, BLUE, YELLOW, WHITE]


#TWINKLE = YELLOW
TURNOVER = 1
TWINKLE_TIME = 6
TWINKLE_TIME = 16

def load_plugin(update_lamps, num_lamps, lamps):
    return GlitterGrey(update_lamps, num_lamps, lamps)

class GlitterGrey(object):
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
        self.base_color = COLOR_WHEEL1[random.randrange(0, len(COLOR_WHEEL1))]
        self.cur_color = self.base_color

        print("num_lamps = {}".format(num_lamps))
        for i in range(0, num_lamps):
            print("i = {}".format(i))
            lamps.colors[i] = self.cur_color
            self.increments.append(random.randrange(20, 427))
        
    def randomColor(self):
        return(COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))])

    def setBrightness(self, brightness):
        self.brightness = brightness

    def interval(self):
        return(self.m_interval)

    def setInterval(self, val):
        self.m_interval = val

    def change(self, lamps):
        haveChange = False
        if time.time() > self.last_time + TURNOVER:
            self.last_time = time.time()
            self.cur_color = self.base_color

        for i in range(0, self.num_lamps):
            self.increments[i] -= 1
            if self.increments[i] <= 0:
                haveChange = True
                if lamps.colors[i].equals(self.base_color):
                    lamps.colors[i] = self.randomColor()
                    self.increments[i] = TWINKLE_TIME
#                    print("FLASH[{}] = {}".format(i, self.increments[i]))
                else:
                    lamps.colors[i] = self.cur_color
                    self.increments[i] = random.randrange(10, 200)
#                    print("inc[{}] = {}".format(i, self.increments[i]))

        if haveChange:
            self.update_lamps(lamps)

        

