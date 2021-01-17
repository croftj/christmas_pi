from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys

COLOR_WHEEL = [RED, CYAN, GREEN, MAGENTA, Color(0, 0, 255), YELLOW, Color(200, 150,0)]

#COLOR_WHEEL = [
#                Color(255, 150, 150)
#              , Color(100, 255, 255)
#              , Color(150, 255, 150)
#              , Color(250, 150, 255)
#              , Color(120, 120, 255)
#              , Color(255, 255, 80)
#            ]

def load_plugin(update_lamps, num_lamps, lamps):
    return RandomFade(update_lamps, num_lamps, lamps)

class RandomFade(object):
    def __init__(self, update_lamps, num_lamps, lamps):
        # custom initialization
        self.increments = []
        self.targets = []
        self.num_lamps = num_lamps
        self.update_lamps = update_lamps
        self.m_interval = .0333      # Interval to be called in milliseconds
        self.brightness = 100
        oc = RED
        for i in range(0, num_lamps):
            nc = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))]
            while nc == oc:
                nc = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))]
            oc = nc
            lamps.colors[i] = nc
            nc = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))]
            while nc == lamps.colors[i]:
                nc = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))]
            self.targets.append(nc)
            self.increments.append(random.randrange(0, 50))
#            print(f"ofs: {i}, cur: {lamps.colors[i].str()},\t** tgt: {self.targets[i].str()}")

    def init(self, lamps):
        return

    def change(self, lamps):
        for i in range(0, self.num_lamps):
            if lamps.colors[i].equals(self.targets[i]):
                if self.increments[i] == 0:
                    nc = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))]
                    while nc == self.targets[i]:
                        nc = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))]
                    self.targets[i] = nc
#                    print(f"ofs: {i}, cur: {lamps.colors[i].str()},\t** tgt: {self.targets[i].str()}")
                    self.increments[i] = random.randrange(0, 15)
                else:
                    self.increments[i] -= 1
            else:
                lamps.colors[i] = lamps.colors[i].step_to(self.targets[i], 3)
        self.update_lamps(lamps)
        

    def interval(self):
        return(self.m_interval)

    def setInterval(self, val):
        self.m_m_interval = val

    def setBrightness(self, brightness):
        self.brightness = brightness


