import colorsys

import datetime
import time

import blinkt

from flask import Flask
app = Flask(__name__)

@app.route("/api/power/<mode>")
def power(mode):
    return "power mode {0}".format(mode)

@app.route("/api/colour/<colour>")
def colour(colour):
    return "colour is {0}".format(colour)

class BlinktController(object):

    def __init__(self):
        self.running = True
        self.pixel = 3
        self.colour = "rainbow"
        self.mode = "off"
        self.colours = {
           "red": Colour(255, 0, 0) 
        }
        blinkt.set_clear_on_exit()
        blinkt.set_brightness(1.0)
        print('init blinkt')

    def run(self):
        print('run')
        while self.running:
            if self.mode == "on":
                if self.colour == "rainbow":
                    self.show_rainbow()
                else:
                    self.show_colour(self.colour)
            time.sleep(0.1)

    def power(self, mode):
        self.mode = mode

    def colour(self, colour):
        self.colour = colour

    def show_rainbow(self):
        hue = int(time.time() * 10) % 360
        offset = 360.0 / 16.0
        h = ((hue + offset) % 360) / 360.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        blinkt.set_pixel(self.pixel, r, g, b)
        blinkt.show()

    def show_colour(self, colour):
        c = self.get_colour(colour)
        blinkt.set_pixel(self.pixel, c.r, c.g, c.b)
        blinkt.show()

    def get_colour(self, colour):
        c = self.colours[colour]
        return c

class Colour(object):

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

controller = BlinktController()

