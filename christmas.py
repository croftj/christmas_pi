from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
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

class Pattern(object):
    def __init__(self, sender, num_lamps, lamps):
        # mandatory variables
        self.sender = sender
        self.num_lamps = num_lamps
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

        print("num_lamps = {}".format(num_lamps))
        for i in range(0, num_lamps):
            print("ia = {}".format(i))
            lamps.colors[i] = self.cur_color
        
        print("num_lamps = {}".format(num_lamps))
        for i in range(0, num_lamps):
            nc = COLOR_WHEEL[random.randrange(0, NUM_COLORS)]
            while i > 0 and nc == self.fixedcolors[i-1]:
                nc = COLOR_WHEEL[random.randrange(0, NUM_COLORS)]

            self.fixedcolors.append(nc)
            self.increments.append(random.randrange(20, 427))
            self.on_times.append(random.randrange(300, 1500))
            lamps.colors[i] = self.fixedcolors[i]
            print("ib = {}, Color({})".format(i, self.fixedcolors[i].str()))
        
    def setBrightness(self, brightness):
        self.brightness = brightness

    def interval(self):
        return(self.t_interval)

    def setInterval(self, val):
        self.t_interval = val

    def change(self, lamps):
        if self.time_count == 0:
            self.time_count = self.change_time
            if self.cur_pattern == 0:
                self.cur_pattern = 1
            else:
                self.cur_pattern = 0
                for i in range(0, self.num_lamps):
                    nc = COLOR_WHEEL[random.randrange(0, NUM_COLORS)]
                    while i > 0 and nc == self.fixedcolors[i-1]:
                        nc = COLOR_WHEEL[random.randrange(0, NUM_COLORS)]

                    self.fixedcolors[i] = nc
                    self.increments[i] = random.randrange(20, 427)
                    self.on_times[i] = random.randrange(300, 1500)
#                    print("ib = {}, Color({})".format(i, self.fixedcolors[i].str()))
        self.time_count = self.time_count - 1
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
        else:
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
#            print("changing lamps @ {}".format(time.time()))
            self.sender[1].dmx_data = lamps.as_list(self.brightness)

        

