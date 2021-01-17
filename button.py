from digitalio import DigitalInOut, Direction, Pull
from enum import Enum
import board
import sys
import time

class ButtonState(Enum):
    SWITCH_OFF      = 0,
    SWITCH_ON       = 1,
    SWITCH_SHORT    = 2,
    SWITCH_LONG     = 3

class Button:
    def __init__(self, iopin, short_time, long_time):
        self.long_time      = long_time
        self.short_time     = short_time
        self.btn            = DigitalInOut(iopin)
        self.btn.direction  = Direction.INPUT
        self.btn.pull       = Pull.UP
        self.timer          = 0
        self.triggered      = False
        self.value          = not self.btn.value
        if self.value:
            self.state = ButtonState.SWITCH_ON
        else:
            self.state = ButtonState.SWITCH_OFF

    def read(self):
        s = not self.btn.value
#        print(f"val = {not self.btn.value}, sval = {self.value}, sstate = {self.state}, tim = {self.timer}")
        if s != self.value:
            time.sleep(.01)
            if s == (not self.btn.value):
                self.value = s
                if not s:
                    self.timer = 0
                    if self.state != ButtonState.SWITCH_OFF:
                        self.triggered = False
                        self.state = ButtonState.SWITCH_OFF
                        return self.state
                    else:
                        return None

                if self.value:
                    self.timer = 0
                    self.state =  ButtonState.SWITCH_ON
                    return self.state
                else:
                    self.timer += 1
                    return None
        elif self.state != ButtonState.SWITCH_OFF:
            if self.timer > self.long_time:
                if self.state != ButtonState.SWITCH_LONG:
                    self.state = ButtonState.SWITCH_LONG
                    return ButtonState.SWITCH_LONG
                elif self.timer > self.long_time + 5:
                    self.timer += 1
                    return None
                else:
                    return None
            elif self.timer > self.short_time:
                if self.state != ButtonState.SWITCH_SHORT:
                    self.state = ButtonState.SWITCH_SHORT
                    return ButtonState.SWITCH_SHORT
                else:
                    self.timer += 1
                    return None
            else:
                self.timer += 1
                return None

        else:
            return None
