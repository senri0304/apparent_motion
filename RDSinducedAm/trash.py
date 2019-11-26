#!/usr/bin/env python
# coding: utf-8

import sys, os, pyglet, time, datetime, copy, random, math
from pyglet.gl import *
from collections import deque
import pandas as pd
import numpy as np
import display_info

# Prefernce
# ------------------------------------------------------------------------
use_scr = 0
rept = 1
exclude_mousePointer = False
data = pd.read_csv("eggs.csv") # Load the condition file
# ------------------------------------------------------------------------

# Get display information
display = pyglet.canvas.get_display()
screens = display.get_screens()

#config = pyglet.gl.Config(sample_buffers=1, samples=4)
config = pyglet.gl.Config()
#window = pyglet.window.Window(config=config, resizable=True)
win = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS, config=config, resizable=True)
win.set_fullscreen(fullscreen=False, screen=screens[use_scr])

key = pyglet.window.key
fixer = pyglet.graphics.Batch()
batch = pyglet.graphics.Batch()
rdss = pyglet.graphics.Batch()

# Load variable conditions
deg1 = display_info.deg1  # 1 deg = 43 pix at LEDCinemaDisplay made by Apple
am42 = display_info.am42  # 42 arcmin = 30 pix
cntx = screens[use_scr].width / 2  # Store center of screen about x positon
cnty = screens[use_scr].height / 2  # Store center of screen about y position
draw_objects = []  # 描画対象リスト
end_routine = False  # Routine status to be exitable or not
tc = 0  # Count transients
tcs = []  # Store transients per trials
trial_starts = []  # Store time when trial starts
kud_list = []  # Store durations of key pressed
cdt = []  # Store sum(kud), cumulative reaction time on a trial.
mdt = []
dtstd = []
exitance = True
n = 0
outer = 9000
#header = data.columns # Store variance name
#ind = dat.shape[0] # Store number of csv file's index
dat = pd.DataFrame()
variable = pd.DataFrame(copy.copy(display_info.variation))
datt = variable.join(data)
header = datt.columns # Store variance name
ind = datt.shape[0] # Store number of csv file's index
#print(dat)

for j in range(rept):
    camp = datt.take(np.random.permutation(ind))
    dat = pd.concat([dat, camp], axis=0, ignore_index=True)
dat = dat.values
dl = dat.shape[0]
print(dat)
#print(dat)
#print(dl)
#variable = copy.copy(display_info.variation)*rept*len(display_info.delay)*len(display_info.lag)
#variable2 = copy.copy(display_info.delay)*rept*len(display_info.variation)*len(display_info.lag)
#variable3 = copy.copy(display_info.lag)*rept*len(display_info.variation)*len(display_info.delay)
#r = random.randint(0, math.factorial(len(variable)))
#random.seed(r)
#sequence = random.sample(variable, len(variable))
#sequence2 = random.sample(variable2, len(variable))
#sequence3 = random.sample(variable3, len(variable))
#print(sequence)
#print(sequence2)
#print(sequence3)

# Load sound resource
# Sounds
os.environ["LD_LIBRARY_PATH"] += ":" + "~/ffmpeg-4.2.1"
pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
p_sound = pyglet.resource.media("material/button57.mp3", streaming=False)
beep_sound = pyglet.resource.media("material/p01.mp3", streaming=False)
# Images # spriteの原点は左下
rds0 = pyglet.image.load("material/rds0.png")
rds1 = pyglet.image.load("material/rds1.png")
rds0_sprite = pyglet.sprite.Sprite(rds0, batch=rdss, y=-2000)
rds1_sprite = pyglet.sprite.Sprite(rds1, batch=rdss, y=-2000)

fixation = pyglet.image.load("material/fixationPoint.png")
fixl = pyglet.sprite.Sprite(fixation, x=cntx - fixation.width / 2.0, y=cnty - fixation.height / 2.0,
                            batch=batch)
bg = pyglet.image.load("material/pedestal.png")
bgl = pyglet.sprite.Sprite(bg, x=cntx - bg.width / 2.0, y=cnty - bg.height / 2.0, batch=fixer)

gray_mask = pyglet.image.load('material/gray_mask.png')
black_mask = pyglet.image.load('material/black_mask.png')
gray = pyglet.sprite.Sprite(gray_mask, x=cntx - deg1*4.5 + 1, y=cnty - gray_mask.height / 2.0)

img = pyglet.image.load("material/WhiteCircle20x20.png")
sprite_left = pyglet.sprite.Sprite(img, batch=batch, y=-200)
sprite2_left = pyglet.sprite.Sprite(img, batch=batch, y=-200)
sprite_left.scale = 0.5
sprite2_left.scale = 0.5
based_left_x = cntx - sprite_left.width / 2.0
based_y = cnty - sprite_left.height / 2.0
displacement = am42/2  # sprite_right.width*2
eccentricity = deg1

displacement_x = copy.copy(displacement) - 0
basedRds_left = cntx - rds0_sprite.width/2 - deg1


def setDefaults():
    global displacement, outer, sequence, sequence2, sequence3
    displacement = am42/2

    da = dat[n]

    sequence = da[0]
    sequence2 = da[1]
    sequence3 = da[2]

    sprite_left.x = (based_left_x + eccentricity + displacement_x - deg1*2)  # 左目鼻側右列
    sprite2_left.x = (based_left_x + eccentricity - displacement_x - deg1*2) # 左目鼻側左列

    rds0_sprite.y = cnty
    rds1_sprite.y = cnty - rds0_sprite.height


def preparation():
    global outer
    pyglet.clock.schedule_once(set_move, sequence3)
    pyglet.clock.schedule_once(set_interval, sequence2)
    pyglet.clock.schedule_once(delete, 30.0)
    rds0_sprite.x = basedRds_left
    rds1_sprite.x = basedRds_left
    outer = 0


def set_move(dt):
    pyglet.clock.schedule_interval(on_move, 0.2)


def update():
    global displacement
    sprite_left.update(y=based_y + displacement)
    sprite2_left.update(y=based_y - displacement)
    return sprite_left, sprite2_left


def update_rds(dt):
    global rds0_sprite, rds1_sprite, rds_d
    rds0_sprite.update(x=basedRds_left + rds_d)
    rds1_sprite.update(x=basedRds_left - rds_d)
    return rds0_sprite, rds1_sprite


def set_interval(dt):
    pyglet.clock.schedule_interval(update_rds, 0.2)


def remove():
    global displacement, outer, rds_d
    displacement = 3000
    rds_d = 3000
    update()
    rds0_sprite.update(x=basedRds_left + rds_d)
    rds1_sprite.update(x=basedRds_left - rds_d)
    fixl.update(y=3000)


# A getting key response function
class key_resp(object):
    def on_key_press(self, symbol, modifiers):
        global tc, exitance, trial_start, outer
        if exitance == False and symbol == key.DOWN:
            kd.append(time.time())
            tc = tc + 1
        if exitance == True and symbol == key.UP:
            exitance = False
            p_sound.play()
 #           pyglet.clock.schedule_interval(on_move, 0.2)
 #           pyglet.clock.schedule_once(delete, 30.0)
 #           rds0_sprite.x = basedRds_left
 #           rds1_sprite.x = basedRds_left
 #           outer = 0
            preparation()
            trial_start = time.time()
        if symbol == key.ESCAPE:
            win.close()
            pyglet.app.exit()

    def on_key_release(self, symbol, modifiers):
        global tc
        if exitance == False and symbol == key.DOWN:
            ku.append(time.time())
            tc = tc + 1
resp_handler = key_resp()


def on_move(dt):
    global displacement, rds_d
    displacement = -1 * displacement
    rds_d = -1 * rds_d
    update()

#clk = 0
#def on_rds(dt):
#    global clk, outer, n
#    clk += (1/30)*0.25*sequence[n]
#    rds_x1 = np.arcsin(np.sin(np.rad2deg(clk)))*20 + basedRds_left + outer
#    rds_x2 = np.arcsin(-np.sin(np.rad2deg(clk)))*20 + basedRds_left + outer
#    rds0_sprite.update(x=rds_x1)
#    rds1_sprite.update(x=rds_x2)
#    return rds0_sprite, rds1_sprite

# Remove stimulus
def delete(dt):
    global n, trial_end, exitance, outer
    exitance = False
    pyglet.clock.unschedule(on_move)
    remove()
    p_sound.play()
    pyglet.clock.schedule_once(exit_routine, 30.0)
    trial_end = time.time()
    pyglet.clock.unschedule(on_move)
    pyglet.clock.unschedule(update_rds)
    get_results()


def exit_routine(dt):
    global exitance
    exitance = True
    beep_sound.play()
    fixl.update(y=cnty - fixl.height / 2.0)
#    fixr.update(y=cnty - fixr.height / 2.0)
    pyglet.app.exit()


def get_results():
    global ku, kud, kd, kud_list, mdt, dtstd, n, tc, tcs, trial_end, trial_start
    ku.append(trial_start + 10.0)
    while len(kd) > 0:
        kud.append(ku.popleft() - kd.popleft() + 0)  # list up key_press_duration
    kud_list.append(str(kud))
    c = sum(kud)
    cdt.append(c)
    tcs.append(tc)
    if kud == []:
        kud.append(0)
    m = np.mean(kud)
    d = np.std(kud)
    mdt.append(m)
    dtstd.append(d)
    n += 1
    print("--------------------------------------------------")
    print("trial: " + str(n) + "/" + str(dl))
    print("start: " + str(trial_start))
    print("end: " + str(trial_end))
    print("key_pressed: " + str(kud))
    print("transient counts: " + str(tc))
    print("cdt: " + str(c))
    print("mdt: " + str(m))
    print("dtstd " + str(d))
    print("condition" + str(sequence))
    print("condition" + str(sequence2))
    print("--------------------------------------------------")
    # Check the experiment continue or break
    if n == dl:
        pyglet.app.exit()


@win.event
def on_draw():
    # Refresh window
    win.clear()
    # 描画対象のオブジェクトを描画する
    fixer.draw()
    rdss.draw()
    gray.draw()
    batch.draw()


# Store the start time
start = time.time()
win.push_handlers(resp_handler)
#pyglet.clock.schedule_interval(on_rds, 1/60)


# ----------------- start loop -----------------------------
# Get variables per trial from csv
for i in range(dl):
    tc = 0  # Count transients
    ku = deque([])  # Store unix time when key up
    kd = deque([])  # Store unix time when key down
    kud = []  # Differences between kd and ku
    rds_d = copy.copy(dat[n, 0])

    # Set up polygon for stimulus
    setDefaults()

    pyglet.app.run()

# -------------- End loop -------------------------------

win.close()

# Store the end time
end_time = time.time()
daten = datetime.datetime.now()

# Write results onto csv
results = pd.DataFrame({'distance': sequence,
                        'delay': sequence2,
                        'lag': sequence3,
                        "transient_counts": tcs,  # Store transient_counts
                        "cdt": cdt,  # Store cdt(target values) and input number of trials
                        "mdt": mdt,
                        "dtstd": dtstd,
                        "key_press_list": kud_list})  # Store the key_press_duration list

if os.path.exists("data") == False:
    os.mkdir("data")

name = str(daten)
name = name.replace(":", "'")
results.to_csv(path_or_buf="./data/DATA" + name + ".csv", index=False)  # Output experimental data

# Output following to shell, check this experiment
print(u"開始日時: " + str(start))
print(u"終了日時: " + str(end_time))
print(u"経過時間: " + str(end_time - start))
