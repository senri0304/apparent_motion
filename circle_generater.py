{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import numpy as np\n",
    "from PIL import Image, ImageDraw\n",
    "\n",
    "to_dir = 'material' \n",
    "os.makedirs(to_dir, exist_ok=True)\n",
    "name = \"WhiteCircle100x100\"\n",
    "\n",
    "# Input RDS's size, caring be dividable \n",
    "x = 100\n",
    "y = 100\n",
    "\n",
    "# Image prepair\n",
    "img = Image.new(\"RGBA\", (x+1, y+1), (0, 0, 0, 0))\n",
    "draw = ImageDraw.Draw(img)\n",
    "draw.ellipse((0, 0, x, y), fill=(255, 255, 255, 255))\n",
    "\n",
    "img = img.resize(size=(x-1, y-1), resample=Image.ANTIALIAS)\n",
    "\n",
    "# Write images\n",
    "basename = os.path.basename(name + '.png')\n",
    "img.save(os.path.join(to_dir, basename), quality=100)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
