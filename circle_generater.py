#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
from PIL import Image, ImageDraw

to_dir = 'material' 
os.makedirs(to_dir, exist_ok=True)
name = "fixationPoint"

# Input size
x = 20
y = 20

# Image prepair
img = Image.new("RGBA", (x+1, y+1), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

draw.ellipse((0, 0, x, y), fill=(255, 255, 255, 255))
#img = img.resize(size=(x, y), resample=Image.ANTIALIAS)

# Write images
basename = os.path.basename(name + '.png')
img.save(os.path.join(to_dir, basename), quality=100)
