import colorsys

import datetime
import time
import threading

import blinkt

from flask import Flask
app = Flask(__name__)

@app.route("/api/power/<mode>", methods=['POST'])
def power(mode):
    controller.set_power(mode)
    return "power mode {0}".format(mode)

@app.route("/api/colour/<colour>", methods=['POST'])
def colour(colour):
    controller.set_colour(colour)
    return "colour is {0}".format(colour)

class BlinktController(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.pixel = 3
        self.colour = "rainbow"
        self.mode = "off"
        self.colours = {
           "red": Colour(255, 0, 0),
           "green": Colour(0, 255, 0),
           "blue": Colour(0, 0, 255),
           "purple": Colour(128, 0, 128),
           "pink": Colour(255, 0, 255),
        }
        self.modes = [
            'on',
            'off',
        ]
        blinkt.set_clear_on_exit()
        blinkt.set_brightness(1.0)

    def run(self):
        while self.running:
            if self.mode == "on":
                if self.colour == "rainbow":
                    self.show_rainbow()
                else:
                    self.show_colour(self.colour)
            else:
                blinkt.clear()
                blinkt.show()
            time.sleep(0.1)

    def set_power(self, mode):
        if mode in self.modes:
            self.mode = mode

    def set_colour(self, colour):
        if colour in self.colours.keys():
            if self.mode == 'off':
                self.mode = 'on'
            self.colour = colour

    def show_rainbow(self):
        hue = int(time.time() * 10) % 360
        offset = 360.0 / 16.0
        h = ((hue + offset) % 360) / 360.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        blinkt.set_pixel(self.pixel, r, g, b)
        blinkt.show()

    def show_colour(self, colour):
        if colour in self.colours.keys():
            c = self.get_colour(colour)
            blinkt.set_pixel(self.pixel, c.r, c.g, c.b)
        else:
            blinkt.clear()
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
controller.start()

