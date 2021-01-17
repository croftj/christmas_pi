import board
import neopixel

class SuperNeoPixel(neopixel.NeoPixel):
    def __init__(self, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None):
        super().__init__(pin, n, brightness=brightness, pixel_order=pixel_order, auto_write=auto_write)

    def set_array(self, colors, brightness = 100):
        ofs = 0
        for color in colors:
            if ofs < self.n:
                self[ofs] = color.as_list(brightness)
            ofs += 1
