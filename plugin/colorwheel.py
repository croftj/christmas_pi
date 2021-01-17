from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys
import time

COLOR_WHEEL = [RED, CYAN, GREEN, MAGENTA, Color(0, 0, 255), YELLOW]

#COLOR_WHEEL = [
#                Color(255, 150, 150)
#              , Color(100, 255, 255)
#              , Color(150, 255, 150)
#              , Color(250, 150, 255)
#              , Color(120, 120, 255)
#              , Color(255, 255, 80)
#            ]
def load_plugin(update_lamps, num_lamps, lamps):
    return Pattern(update_lamps, num_lamps, lamps)

class Pattern(object):
    def __init__(self, update_lamps, num_lamps, lamps):
        # custom initialization
        self.increments = []
        self.last_color = cur_color = random.randrange(0, len(COLOR_WHEEL))
        i = 0
        for color in COLOR_WHEEL:
            self.increments.append(1)
            i = i + 1
        print("len(COLOR_SHEEL) = {}".format(len(COLOR_WHEEL)))
        # mandatory variables
        self.num_lamps = num_lamps
        self.update_lamps = update_lamps
        self.m_interval = 300 * 1000      # Interval to be called in milliseconds
        self.brightness = 100

    def interval(self):
        return(self.m_interval)

    def setInterval(self, val):
        self.m_m_interval = val

    def setBrightness(self, brightness):
        self.brightness = brightness

    def init(self, lamps):
        return

    def change(self, lamps):
        color = (self.last_color + self.increments[self.last_color]) % len(COLOR_WHEEL)
        inc = self.increments[self.last_color] + 1
        if inc >= len(COLOR_WHEEL):
            inc = 1
        self.increments[self.last_color] = inc
#        print("color = {}, increment[{}] = {}".format(color, self.last_color, self.increments[self.last_color]))
#        print("color = {}, increment[{}] = {}: {}".format(color, self.last_color, self.increments[self.last_color], COLOR_WHEEL[color].str()))
        self.last_color = color
        while not lamps.colors[0].equals(COLOR_WHEEL[color]):
            self.update_lamps(lamps)
            time.sleep(.06)
        

