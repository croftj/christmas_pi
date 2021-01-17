from LEDColors.Colors import RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, BLACK, Color, ColorArray
import os
import random
import sys
import math
import time

WHITE = Color(150, 150, 150)

def clamp(val, v_min, v_max):
#    print(f"val: {val}, min: {v_min}, max: {v_max}")
    return(max(min(v_max, val), v_min))


##############################################################
# Plugin function that creates an instance of the plugin     #
# object (in this case CandyCane) and returns its reference. #
#                                                            #
# See __init__() below for the arguments to this function.   #
##############################################################
def load_plugin(update_lamps, num_lamps, lamps):
    return CandyCane(update_lamps, num_lamps, lamps)

class CandyCane(object):

    #########################################################
    # Function called in construction of a new object.      #
    #                                                       #
    # Parameters:                                           #
    #                                                       #
    #     update_lamps    Reference to a function that      #
    #     will update the actual LED array with the new     #
    #     lamp values.                                      #
    #                                                       #
    #     num_lamps       The number of lamps in the string #
    #                                                       #
    #     lamps           An Object with an array named     #
    #     colors that holds the color inforation for each   #
    #     lamp in the string                                #
    #
    # Returns:                                              #
    #   Nothing                                             #
    #########################################################
    def __init__(self, update_lamps, num_lamps, lamps):
        # mandatory variables
        self.num_lamps = num_lamps
        self.update_lamps = update_lamps
        self.m_interval = .2    # Interval to be called in seconds
        self.brightness = 100   # Default brightness (0 - 100%)

        # custom initialization
        self.increments = []
        self.states = []
        self.colors = []
        self.last_time = time.time()
        self.state = True
        self.start_cnt = 0
        self.start_red = True
        self.stripe_len = self.num_lamps / 15
        print("num_lamps = {}".format(num_lamps))

    ######################################################
    # Used to set the overall brightness for the pattern #
    ######################################################
    def setBrightness(self, brightness):
        self.brightness = brightness

    ###################################################
    # returns the value of the current setting of the #
    # interval                                        #
    ###################################################
    def interval(self):
        return(self.m_interval)

    ###########################################################
    # Used to set the interval in which the change() function #
    # will be called                                          #
    ###########################################################
    def setInterval(self, val):
        self.m_interval = val

    ########################################################
    # To be called after the instance of the plugin is     #
    # created to set any initial state of the plugin. This #
    # will be called by the controller once everytime the  #
    # plugin is activated.                                 #
    ########################################################
    def init(self, lamps):
        return

    #########################################################
    # Called periodically (as defined by self.interval)     #
    # to update the lamps.                                  #
    #                                                       #
    # The parameter lamps should be a reference to the lamp #
    # object. Within it is an array of LEDColors that can   #
    # be accessed though the member variable colors.        #
    #                                                       #
    # To help optimize the possible CPU and Network traffic #
    # associated in sending out the color array when no     #
    # changes have been made, self.udate_lamps() must be    #
    # called before returning from this function.           #
    #########################################################
    def change(self, lamps):
#        print("here")
        haveChange = False
        if True:
            count = self.start_cnt
            current_red = self.start_red
            for index in range(1, self.num_lamps - 1):
                if current_red:
                    lamps.colors[index] = RED
                else:
                    lamps.colors[index] = WHITE
                count += 1
                if count > self.stripe_len:
                    count = 0
                    current_red = True if current_red == False else False
            self.start_cnt -= 1
            if self.start_cnt < 0:
                self.start_cnt = self.stripe_len
                self.start_red = True if self.start_red == False else False

        self.update_lamps(lamps)
