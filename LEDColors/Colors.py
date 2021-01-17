########################################################
# This class represents a color with an Red, Green and #
# Blue element.                                        #
########################################################
class Color(object):
    #######################################################
    # Instantiates the color object with an inition value #
    # represented by the integers in the parameters r, g, #
    # and b                                               #
    #######################################################
    def __init__(self, r = 0, g = 0, b = 0):
        self.r = r % 256
        self.g = g % 256
        self.b = b % 256

    #######################################################
    # Tests for equality between the color values of this #
    # color and the alt_color object.                     #
    #                                                     #
    # Returns true if they match, false otherwise.        #
    #######################################################
    def equals(self, alt_color):
        if self.r == alt_color.r and \
           self.g == alt_color.g and \
           self.b == alt_color.b:
            return(True)
        else:
            return(False)

    ###########################################################
    # Returns the color as an array of three integers         #
    # representing this objects color that have been scaled.  #
    #                                                         #
    # The parameter scale is a value from 0 to 100 that will  #
    # adjust the brightness of the color from off to full on. #
    ###########################################################
    def as_list(self, scale = 100):
        rv = []
        rv.append(int(self.r * scale / 100) % 256)
        rv.append(int(self.g * scale / 100) % 256)
        rv.append(int(self.b * scale / 100) % 256)
        return(rv)

    ###########################################################
    # Returns a human readable string indicating the 3 values #
    # of the color/                                           #
    ###########################################################
    def str(self, scale = 100):
        return("r: {}, g: {}, b: {}".format(self.r * scale / 100, self.g * scale / 100, self.b * scale / 100))

    #########################################################
    # This function returns the value of the color after it #
    # has been incremented by step toward the target color. #
    # The returned color will never increment past the      #
    # target color.                                         #
    #########################################################
    def step_to(self, target, step):
        rv = Color(self.r, self.g, self.b)
        if (target.r >= rv.r + step):
            rv.r = rv.r + step
        elif (target.r <= rv.r - step):
            rv.r = rv.r - step
        else:
            rv.r = target.r

        if (target.g >= rv.g + step):
            rv.g = rv.g + step
        elif (target.g <= rv.g - step):
            rv.g = rv.g - step
        else:
            rv.g = target.g

        if (target.b >= rv.b + step):
            rv.b = rv.b + step
        elif (target.b <= rv.b - step):
            rv.b = rv.b - step
        else:
            rv.b = target.b

        return(rv)

############################
# Predefined color objects #
############################
RED     = Color(255, 0, 0)
BLUE    = Color(0, 0, 150)
GREEN   = Color(0, 255, 0)
CYAN    = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
YELLOW  = Color(255, 255, 0)
BLACK   = Color(0, 0, 0)

#############################################################
# This object creates an array of Color objects. The length #
# of the array is defined by size and the initial color is  #
# defined by init_color                                     #
#############################################################
class ColorArray(object):
    def __init__(self, size = 170, init_color = BLACK):
        self.colors = []
        for n in range(0, size):
#            print("n = {}".format(n))
            self.colors.append(init_color)

    def value(self, index):
        return(self.colors[index])

    ##########################################################
    # returns a list of integer values the make up the array #
    # of colrs. The array is ordered Red, Green, Blue for    #
    # each color in the ColorArray                           #
    #                                                        #
    # The values are scaled by the value scale which can     #
    # range between 0 and 100.                               #
    ##########################################################
    def as_list(self, scale = 100):
        rv = []
#        print("tgt: {}".format(self.colors[0].str(scale)))
        for n in range(0, len(self.colors)):
            color = self.colors[n].as_list(scale)
#            print("n = {}".format(n))
            for i in color:
                rv.append(i)

#        for i in rv:
#            print("i = {}".format(i))
        return(rv)

    def set_color(self, index, color):
        self.colors[index] = Color(color.r, color.g, color.b)

