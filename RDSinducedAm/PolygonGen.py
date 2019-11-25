#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
from PIL import Image, ImageDraw
from display_info import *

to_dir = 'material'
os.makedirs(to_dir, exist_ok=True)

# Input RDS's size, caring be dividable
height = round(deg1*0.3125)
width = round(deg1*1.5)

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
            x = np.round(np.random.binomial(1, 0.5, 1)) * j
            draw.point((x - 1, i), fill=ld)

    img_resize = img.resize((int(img.width*2), int(img.height*2)))

    # Write images
    basenameR = os.path.basename('rds' + str(k) + '.png')
    img_resize.save(os.path.join(to_dir, basenameR), quality=100)



sz = round(resolution * (5 / d_height))
f = round(sz*0.023) # % relative size


# Mask
img = Image.new('LA', (sz + deg1*2, round(height*4)), 0)
draw = ImageDraw.Draw(img)

draw.rectangle((deg1*4.2, 0, sz + deg1*2, round(height*4)), fill=(lb, 255))
draw.rectangle((0, 0, deg1*2, round(height*4)), fill=(0, 255))
draw.rectangle((deg1*2, 0, deg1*2.75, round(height*4)), fill=(lb, 255))
img.save(os.path.join(to_dir, 'gray_mask.png'))

#img = Image.new('L', (round(deg1+1), round(height*4)), 0)
#draw = ImageDraw.Draw(img)
#img.save(os.path.join(to_dir, 'black_mask.png'))


# stereogram without stimuli
img = Image.new("L", (sz, sz), lb)
draw = ImageDraw.Draw(img)

basename = os.path.basename('pedestal.png')
img.save(os.path.join(to_dir, basename), quality=100)


# fixation point
img = Image.new("RGBA", (round(f*3)+1, round(f*3)+1), 0)
draw = ImageDraw.Draw(img)
draw.rectangle((0, round(f),
                round(f*3+1), round(f*2)),
               fill=(0, 0, 255), outline=None)
draw.rectangle((round(f), 0,
                round(f*2), round(f*3+1)),
               fill=(0, 0, 255), outline=None)

basename = os.path.basename('fixationPoint.png')
img.save(os.path.join(to_dir, basename), quality=100)