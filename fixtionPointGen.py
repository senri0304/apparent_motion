import os
import numpy as np
from PIL import Image, ImageDraw

to_dir = 'material' 
os.makedirs(to_dir, exist_ok=True)
name = "fixationPoint"

# Input size
x = 15
y = 15

# Image prepair
img = Image.new("RGBA", (x+1, y+1), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.rectangle((0, 5, 15, 10), fill=(0, 0, 255, 255))
draw.rectangle((5, 0, 10, 15), fill=(0, 0, 255, 255))

# Write images
basename = os.path.basename(name + '.png')
img.save(os.path.join(to_dir, basename), quality=100)
