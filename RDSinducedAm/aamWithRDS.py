#!/usr/bin/env python
# coding: utf-8

import sys, os, pyglet, time, datetime, copy
from pyglet.gl import *
from collections import deque
import pandas as pd
import numpy as np

# Prefernce
# ------------------------------------------------------------------------
use_scr = 0
rept = 3
data = pd.read_csv("eggs.csv")  # Load the condition file
exclude_mousePointer = False
# ------------------------------------------------------------------------

# Get display informations
display = pyglet.canvas.get_display()
screens = display.get_screens()
win = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
win.set_fullscreen(fullscreen=True, screen=screens[use_scr])
key = pyglet.window.key
fixer = pyglet.graphics.Batch()
batch = pyglet.graphics.Batch()
rdss = pyglet.graphics.Batch()

# Load variable conditions
header = data.columns  # Store variance name
ind = data.shape[0]  # Store number of csv file's index
dat = pd.DataFrame()
list_a = []  # Create null list to store experimental variance
list_b = []
list_c = []
list_d = []
deg1 = 43.0  # 1 deg = 43 pix at LEDCinemaDisplay made by Apple
am42 = 30.0  # 42 arcmin = 30 pix
iso = 7
cntx = screens[use_scr].width / 2  # Store center of screen about x positon
cnty = screens[use_scr].height / 3  # Store center of screen about y position
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

# Load sound resource
## Sounds
os.environ["LD_LIBRARY_PATH"] += ":" + "~/ffmpeg-4.2.1"
pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
p_sound = pyglet.resource.media("material/button57.mp3", streaming=False)
beep_sound = pyglet.resource.media("material/p01.mp3", streaming=False)
##Images # spriteの原点は左下
rds0 = pyglet.image.load("material/rds0.png")
rds1 = pyglet.image.load("material/rds1.png")
rds0_sprite = pyglet.sprite.Sprite(rds0, batch=rdss, y=-200)
rds1_sprite = pyglet.sprite.Sprite(rds1, batch=rdss, y=-200)

fixation = pyglet.image.load("material/fixationPoint.png")
fixr = pyglet.sprite.Sprite(fixation, x=cntx + iso * deg1 - fixation.width / 2.0, y=cnty - fixation.height / 2.0,
                            batch=batch)
fixl = pyglet.sprite.Sprite(fixation, x=cntx - iso * deg1 - fixation.width / 2.0, y=cnty - fixation.height / 2.0,
                            batch=batch)
bg = pyglet.image.load("material/bg.png")
bgr = pyglet.sprite.Sprite(bg, x=cntx + iso * deg1 - bg.width / 2.0, y=cnty - bg.height / 2.0, batch=fixer)
bgl = pyglet.sprite.Sprite(bg, x=cntx - iso * deg1 - bg.width / 2.0, y=cnty - bg.height / 2.0, batch=fixer)

msk = pyglet.image.load('material/mask.png')
mask = pyglet.sprite.Sprite(msk, x=cntx - iso * deg1 - msk.width + 48, y=cnty - msk.height / 2.0)

img = pyglet.image.load("material/WhiteCircle6x6.png")
sprite_right = pyglet.sprite.Sprite(img, batch=batch, y=-200)
sprite2_right = pyglet.sprite.Sprite(img, batch=batch, y=-200)
sprite_left = pyglet.sprite.Sprite(img, batch=batch, y=-200)
sprite2_left = pyglet.sprite.Sprite(img, batch=batch, y=-200)
sprite3_right = pyglet.sprite.Sprite(img, batch=batch, y=-200)
sprite4_right = pyglet.sprite.Sprite(img, batch=batch, y=-200)
sprite3_left = pyglet.sprite.Sprite(img, batch=batch, y=-200)
sprite4_left = pyglet.sprite.Sprite(img, batch=batch, y=-200)
based_right_x = cntx + deg1 * iso - sprite_right.width / 2.0
based_left_x = cntx - deg1 * iso - sprite_left.width / 2.0
based_y = cnty - sprite_left.height / 2.0
displacement = 30  # sprite_right.width*2
eccentricity = 100

# sprite5_left = pyglet.sprite.Sprite(img, batch=batch, x=based_right_x + eccentricity, y=based_y)
# sprite6_left = pyglet.sprite.Sprite(img, batch=batch, x=based_right_x - eccentricity, y=based_y)
# sprite7_left = pyglet.sprite.Sprite(img, batch=batch, x=based_left_x + eccentricity, y=based_y)
# sprite8_left = pyglet.sprite.Sprite(img, batch=batch, x=based_left_x - eccentricity, y=based_y)


displacement_x = copy.copy(displacement) - 0
basedRds_left = based_left_x - rds0_sprite.width - displacement_x


def setDefaults():
    global displacement, dr, dl, pr, pl, outer
    displacement = 30
    sprite_right.x = (based_right_x + eccentricity + displacement_x - dr) * pr  # 右目耳側右列
    sprite2_right.x = (based_right_x + eccentricity - displacement_x - dl) * pr  # 右目耳側左列
    sprite_left.x = (based_left_x + eccentricity + displacement_x + dr) * pr  # 左目鼻側右列
    sprite2_left.x = (based_left_x + eccentricity - displacement_x + dl) * pr  # 左目鼻側左列

    sprite3_right.x = (based_right_x - eccentricity + displacement_x)  # 右目鼻側右列
    sprite4_right.x = (based_right_x - eccentricity - displacement_x)  # 右目鼻側左列
    sprite3_left.x = (based_left_x - eccentricity + displacement_x)  # 左目耳側右列
    sprite4_left.x = (based_left_x - eccentricity - displacement_x)  # 左目耳側左列

    rds0_sprite.y = cnty
    rds1_sprite.y = cnty - rds0_sprite.height


def update():
    global displacement, sync
    sprite_right.y = based_y + displacement
    sprite2_right.y = based_y - displacement
    sprite_left.y = based_y + displacement
    sprite2_left.y = based_y - displacement

    sprite3_right.y = based_y + displacement * sync
    sprite4_right.y = based_y - displacement * sync
    sprite3_left.y = based_y + displacement * sync
    sprite4_left.y = based_y - displacement * sync


def remove():
    global displacement, outer
    displacement = 3000
    update()
    fixl.update(y=3000)
    fixr.update(y=3000)
    outer = 3000


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
            pyglet.clock.schedule_interval(on_move, 0.25)
            pyglet.clock.schedule_once(delete, 60.0)
            rds0_sprite.x = basedRds_left
            rds1_sprite.x = basedRds_left
            outer = 0
            #            pyglet.clock.schedule_once(Get_results, 31.0)
            trial_start = time.time()
        if symbol == key.ESCAPE:
            win.close()
            pyglet.app.exit()

    def on_key_release(self, symbol, modifiers):
        global tc
        if exitance == False and symbol == key.DOWN:
            ku.append(time.time())
            tc = tc + 1
            tc = tc + 1


resp_handler = key_resp()


def on_move(dt):
    global displacement
    displacement = -1 * displacement
    update()

outer = 1920
clk = 0
def on_rds(dt):
    global clk, outer
    clk += (1/60)*0.25
    rds_x1 = np.arcsin(np.sin(np.rad2deg(clk)))*20 + basedRds_left + 25 + outer
    rds_x2 = np.arcsin(-np.sin(np.rad2deg(clk)))*20 + basedRds_left + 25 + outer
    rds0_sprite.update(x=rds_x1)
    rds1_sprite.update(x=rds_x2)
    return rds0_sprite, rds1_sprite


#    global distance
#    destination = based_left_x + distance
#    if rds0_sprite.x == destination:
#        destination = -1 * distance
#    if rds0_sprite.x < destination:
#        rds0_sprite.x += 1
#        rds1_sprite.x -= 1
#    elif rds0_sprite.x > destination:
#        rds0_sprite.x -= 1
#        rds1_sprite.x += 1

# def on_rds(dt):
#    global destination
#    if destination >= based_left_x + displacement:
#        rds0_sprite.x += 1
#        rds1_sprite.x -= 1
#    elif destination >= based_left_x + displacement:
#        rds0_sprite.x -= 1
#        rds1_sprite.x += 1

# Remove stimulus
def delete(dt):
    global n, dl, trial_end
    exitance = False
    pyglet.clock.unschedule(on_move)
    remove()
    p_sound.play()
    pyglet.clock.schedule_once(exit_routine, 30.0)
    trial_end = time.time()
    Get_results()


def exit_routine(dt):
    global exitance
    exitance = True
    beep_sound.play()
    fixl.update(y=cnty - fixl.height / 2.0)
    fixr.update(y=cnty - fixr.height / 2.0)
    pyglet.app.exit()


def Get_results():
    global ku, kud, kd, kud_list, mdt, dtstd, n, tc, tcs, trial_end, trial_start
    ku.append(trial_start + 60.0)
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
    print("trial: " + str(n) + "/" + str(len(dat)))
    print("start: " + str(trial_start))
    print("end: " + str(trial_end))
    print("key_pressed: " + str(kud))
    print("transient counts: " + str(tc))
    print("cdt: " + str(c))
    print("mdt: " + str(m))
    print("dtstd " + str(d))
    print("condition" + str(da))
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
    mask.draw()
    batch.draw()


# Store the start time
start = time.time()
win.push_handlers(resp_handler)
pyglet.clock.schedule_interval(on_rds, 1/60)


# ----------------- start loop -----------------------------
# Get variables per trial from csv
for j in range(rept):
    camp = data.take(np.random.permutation(ind))
    dat = pd.concat([dat, camp], axis=0, ignore_index=True)
dat = dat.values
dl = dat.shape[0]
for i in range(dl):
    tc = 0  # Count transients
    ku = deque([])  # Store unix time when key up
    kd = deque([])  # Store unix time when key down
    kud = []  # Differences between kd and ku
    da = dat[i]
    list_a.append(da[0])
    list_b.append(da[1])
    list_c.append(da[2])
    list_d.append(da[3])

    pr = da[1]  # 右視野に表示するかしないか
    pl = da[0]  # 左視野に表示するかしないか
    dr = da[2]  # 右列の視差
    dl = 0  # 左列の視差
    sync = da[3]

    # Set up polygon for stimulus
    setDefaults()

    pyglet.app.run()

# -------------- End loop -------------------------------

win.close()

# Store the end time
end_time = time.time()
daten = datetime.datetime.now()

# Write results onto csv
results = pd.DataFrame({header[0]: list_a,  # Store variance_A conditions
                        header[1]: list_b,  # Store variance_B conditions
                        header[2]: list_c,
                        header[3]: list_d,
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
