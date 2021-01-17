from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys
import time

#TWINKLE = YELLOW
BLACK = Color(0, 0, 0)
COLOR_WHEEL = [RED, GREEN, MAGENTA, BLUE]
NUM_COLORS = len(COLOR_WHEEL)

def load_plugin(update_lamps, num_lamps, lamps):
    return Drip(update_lamps, num_lamps, lamps)

class Drip(object):
    def __init__(self, update_lamps, num_lamps, lamps):
        # mandatory variables
        self.num_lamps = num_lamps
        self.update_lamps = update_lamps
        self.t_interval = .001      # Interval to be called in seconds
        self.change_time = 9000
        self.time_count = self.change_time
        self.cur_pattern = 0

        # custom initialization
        self.colors = []
        self.current_lamp = self.num_lamps - 1
        self.start_color = YELLOW
        self.target_color = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))];
        self.brightness = 100
        self.last_time = time.time()
        self.off_color = Color(30, 30, 0)
        self.running = False
        self.start_count = 1

#        print("num_lamps = {}".format(num_lamps))
        for i in range(0, self.num_lamps):
#            print("ia = {}".format(i))
            lamps.colors[i] = self.off_color
        
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
        black_cnt = 0
        if self.running:
            for i in range(0, self.num_lamps):
                if lamps.colors[i].equals(self.off_color):
                    black_cnt += 1
            if black_cnt >= self.num_lamps - 1:
                self.current_lamp = self.num_lamps - 1
                self.start_color = YELLOW
                self.running = False
                self.start_count - random.randrange(300, 3000)
                self.target_color = COLOR_WHEEL[random.randrange(0, len(COLOR_WHEEL))];
#                print(f"start_count = {self.start_count}")
#            else:
#                print(f"black_cnt = {black_cnt}, current_lamp: {self.current_lamp}, black = {BLACK.str()}")

        if self.start_count > 0:
            self.start_count -= 1
        elif not self.running:
            if lamps.colors[self.num_lamps - 1].equals(self.start_color):
                self.running = True
            else:
                ofs = 0
                for i in range(0, int(self.num_lamps / 20)):
                    ofs = self.num_lamps - i - 1
                    lamps.colors[ofs] = lamps.colors[ofs].step_to(self.start_color, 20)
#                    print(f"color[{ofs}] = {lamps.colors[ofs].str()}")
        elif self.current_lamp >= 0:
            for i in range(self.current_lamp, self.current_lamp - 10, -1):
                self.start_color = self.start_color.step_to(self.target_color, int(self.num_lamps / 120))
                lamps.colors[i] = self.start_color
            self.current_lamp -= 10
#            print(f"current_lamp = {self.current_lamp}")
#            if self.current_lamp <= 0:
#                self.current_lamp  = self.num_lamps - 1
#            for i in range(self.num_lamps - 1, self.current_lamp, -1):
        if self.running:
            for i in range(self.num_lamps - 1, 0,  -1):
                ofs = i
                lamps.colors[ofs] = lamps.colors[ofs].step_to(self.off_color, int(self.num_lamps / 120))
#                if ofs == 5:
#                    print(f"color[{ofs}] = {lamps.colors[ofs].str()}")
        self.update_lamps(lamps)

