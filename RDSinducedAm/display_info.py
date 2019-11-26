#!/usr/bin/env python
# coding: utf-8

import pyglet.canvas

# Input display information
inch = 12
aspect_width = 16
aspect_height = 10

# Get display information
display = pyglet.canvas.get_display()
screens = display.get_screens()

resolution = screens[len(screens) - 1].height

c = (aspect_width ** 2 + aspect_height ** 2) ** 0.5
d_height = 2.54 * (aspect_height / c) * inch

deg1 = round(resolution * (1 / d_height))

am42 = round(resolution * (0.7 / d_height))


variation = [resolution*(0.01/d_height), resolution*(0.05/d_height),
             resolution*(0.1/d_height), resolution*(0.7/d_height)]
distance = [am42/2, am42/4]