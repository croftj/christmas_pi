from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys

COLOR_WHEEL = [RED, CYAN, GREEN, MAGENTA, BLUE, YELLOW]

def load_plugin(update_lamps, num_lamps, lamps):
    return Pattern(update_lamps, num_lamps, lamps)

class Pattern(object):
    def __init__(self, update_lamps, sender, num_lamps):
        # custom initialization
        self.increments = []
        self.last_color = cur_color = random.randrange(0, len(COLOR_WHEEL))
        i = 0
        for color in COLOR_WHEEL:
            self.increments.append(1)
            i = i + 1

        # mandatory variables
        self.sender = sender
        self.num_lamps = num_lamps
        self.update_lamps = update_lamps
        self.interval = 300 * 1000      # Interval to be called in milliseconds

    def interval(self):
        return(self.interval)

    def init(self, lamps):
        return

    def change(self, lamps):
        color = (self.last_color + self.increments[self.last_color]) % len(COLOR_WHEEL)
        inc = self.increments[self.last_color] + 1
        if inc >= len(COLOR_WHEEL):
            inc = 1
        self.increments[self.last_color] = inc
        print("color = {}, increment[{}] = {}".format(color, self.last_color, self.increments[self.last_color]))
        self.last_color = color
        while not lamps.colors[0].equals(COLOR_WHEEL[color]):
    #        print("cur: {}, tgt: {}".format(lamps.colors[0].str(), color.str()))
            for i in range(0, self.num_lamps):
                lamps.colors[i] = lamps.colors[i].step_to(COLOR_WHEEL[color], 3)
            self.update_lamps(lamps)
            time.sleep(.06)
        

