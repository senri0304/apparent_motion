#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
import sys, os, pyglet
from pyglet.gl import *

# Get display informations
display = pyglet.canvas.get_display()
screens = display.get_screens()
win = pyglet.window.Window()

batch = pyglet.graphics.Batch()

# Load sound resource
img = pyglet.image.load("material/WhiteCircle50x50.png")
sprite = pyglet.sprite.Sprite(img, x=300, y=300, batch=batch)
sprite2 = pyglet.sprite.Sprite(img, x=100, y=100, batch=batch)


def on_move(dt):
    if sprite.x != 300:
        sprite.x = 300
        sprite.y = 300
        sprite2.x = 100
        sprite2.y = 100
    else:
        sprite.x = 100
        sprite.y = 300
        sprite2.x = 300
        sprite2.y = 100

@win.event
def on_draw():
    # Refresh window
    win.clear()
    # 描画対象のオブジェクトを描画する
    batch.draw()

pyglet.clock.schedule_interval(on_move, 0.2)

pyglet.app.run()


# In[ ]:





# In[ ]:




