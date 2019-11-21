#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
from PIL import Image, ImageDraw

to_dir = 'material'
os.makedirs(to_dir, exist_ok=True)

# Input RDS's size, caring be dividable
height = 25
width = 100

# Input the disparity at pixel units.
disparity = 0

# Input the quantity you need
q = 2

# Input a number you like to initiate
s = 0

# Input luminance of background
lb = 120 # 215, 84%

# Input luminance of dots
ld = 65

# Generate RDSs
for k in range(q):

    # Two images prepair
    img = Image.new("L", (width, height), lb)
    draw = ImageDraw.Draw(img)


    # Draw the planes of RDSs
    for i in range(0, height):
        for j in range(1, width + 1):
            x = np.round(np.random.binomial(1, 0.5, 1)) * (j)
            draw.point((x - 1, i), fill=(ld))

    img_resize = img.resize((int(img.width*2), int(img.height*2)))

    # Write images
    basenameR = os.path.basename('rds' + str(k) + '.png')
    img_resize.save(os.path.join(to_dir, basenameR), quality=100)

# Mask
img = Image.new('LA', (300, height*4), 0)
draw = ImageDraw.Draw(img)

draw.rectangle((199, 0, 300, 100), fill=(lb, 255))
draw.rectangle((0, 0, 100, 100), fill=(0, 255))

img.save(os.path.join(to_dir, 'mask.png'))