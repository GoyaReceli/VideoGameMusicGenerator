## USE A JOYSTICK TO CONTROL THE INTENSITY AND WINNING VALUES MANUALLY
## LEFT STICK CONTROLS INTENSITY AND RIGHT STICK CONTROLS WINNING STATUS

import sys
import pygame as pg
from pygame.locals import *
import numpy as np
from dictionaries import *
import time
import random
import re

## Setting up pygame
startX = 1200
startY = 800
WIN = pg.display.set_mode((int(startX), int(startY)))
pg.display.set_caption("Adaptive Dynamic Music")
pg.init()
pg.mixer.init()


## Setting up the joystick
pg.joystick.init()
joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]


## Setting up the pitch & interval arrays
frequencies = {}
for key in pitches:
    val = pitches.get(key)
    frequencies[val] = key
notes = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
def get_interval(note1, note2):
    index1 = notes.index(note1)
    index2 = notes.index(note2)
    return (index2 - index1) % 12
clashing_sounds = (1, 2, 10, 11)
minor_sounds = (3, 8)
perfect_sounds = (5, 7)
major_sounds = (4, 9)


## Setting up the tempo. ENTER THE INTENDED TEMPO HERE.
bpm = float(60)
def bps():
    global bpm
    return float(60 / bpm)


## Sound Creater Method ##
## Adopted from:
##              Title: Python_Synth
##              Author: FinFetChannel
##              Accessed Date: 25 June 2020
##              Availability: https://github.com/FinFetChannel/Python_Synth
def synth(frequency, duration=5.0, sampling_rate=44100):
    frames = int(duration * sampling_rate)
    arr = np.cos(2 * np.pi * frequency * np.linspace(0, duration, frames))
    arr = arr + np.cos(4 * np.pi * frequency * np.linspace(0, duration, frames))
    # arr = arr - np.cos(6 * np.pi * frequency * np.linspace(0, duration, frames))
    # arr = np.clip(arr * 10, -1, 1)  # squarish waves
    # arr = np.cumsum(np.clip(arr*10, -1, 1)) # triangularish waves pt1
    # arr = arr+np.sin(2*np.pi*frequency*np.linspace(0,duration, frames)) # triangularish waves pt1
    arr = arr / max(np.abs(arr))  # triangularish waves pt1
    sound = np.asarray([32767 * arr, 32767 * arr]).T.astype(np.int16)
    sound = pg.sndarray.make_sound(sound.copy())
    sound.set_volume(0.33)
    sound.fadeout(50)
    return sound


## MAIN ALGORITHM
def next_note(note_chang, note1, note2, note3):
    note1_split = re.split('(\d+)', note1)[0]
    note2_split = re.split('(\d+)', note2)[0]
    note3_split = re.split('(\d+)', note3)[0]
    notes_tuple = (note1, note2, note3)
    print(notes_tuple)
    curr_notes = (note1_split, note2_split, note3_split)
    fix_interval = []
    note_to_change = None
    for i in range(3):
        if i != note_chang:
            fix_interval.append(curr_notes[i])
        else:
            note_to_change = notes_tuple[i]
    fixed_interval = get_interval(fix_interval[0], fix_interval[1])
    if fixed_interval > 6:
        temp = fix_interval[0]
        fix_interval[0] = fix_interval[1]
        fix_interval[1] = temp
        fixed_interval = 12 - fixed_interval

    next_note = None
    if fixed_interval in clashing_sounds:
        next_note = clashing_next_note(fix_interval, fixed_interval)
    else:
        next_note = find_third_in_chord(fix_interval, fixed_interval)
    result = closest_octave(note_to_change, notes[next_note])
    return result

def clashing_next_note(fix_interval, interval_no):
    global intensity
    global winning_status
    if random.random() < intensity:  ## Clashing sound
        rand_clashing_sound = random.choice(range(4))
        return ((notes.index(fix_interval[1]) + clashing_sounds[rand_clashing_sound]) % 12)
    if winning_status < 0.5:
        rand_sound = random.choice(range(2))
        if random.random() / 2 < winning_status:
            return ((notes.index(fix_interval[1]) + perfect_sounds[rand_sound]) % 12)
        else:
            return ((notes.index(fix_interval[1]) + minor_sounds[rand_sound]) % 12)
    else:
        rand_sound = random.choice(range(2))
        if (0.5 + (random.random() / 2)) < winning_status:
            return ((notes.index(fix_interval[1]) + major_sounds[rand_sound]) % 12)
        else:
            return ((notes.index(fix_interval[1]) + perfect_sounds[rand_sound]) % 12)

def find_third_in_chord(fix_interval, interval_no):
    global intensity
    global winning_status

    if random.random() < intensity:
        return clashing_next_note(fix_interval, interval_no)

    rand = random.random()
    if interval_no == 0:  # Unison
        return ((notes.index(fix_interval[1]) + 7) % 12)
    elif interval_no == 3:  # m3
        if rand <= winning_status:
            return ((notes.index(fix_interval[0]) - 4) % 12)
        else:
            return ((notes.index(fix_interval[1]) + 4) % 12)
    elif interval_no == 4:  # M3
        if rand <= winning_status:
            return ((notes.index(fix_interval[1]) + 3) % 12)
        else:
            return ((notes.index(fix_interval[0]) - 3) % 12)
    elif interval_no == 5:  # P4
        if rand <= winning_status:
            return ((notes.index(fix_interval[1]) + 4) % 12)
        else:
            return ((notes.index(fix_interval[1]) + 3) % 12)
    elif interval_no == 6:  # A4/d5
        if rand <= 0.5:
            return ((notes.index(fix_interval[0]) - 3) % 12)
        else:
            return ((notes.index(fix_interval[0]) + 3) % 12)
    return None

def closest_octave(prev_note, note):
    note_octave = re.split('(\d+)', prev_note)
    interval = get_interval(note_octave[0], note)
    note_string = None
    if interval < 6 or int(note_octave[1]) >= 5:
        note_string = note + str(note_octave[1])
    else:
        note_string = note + str(int(note_octave[1]) + 1)
    return note_string


## Setting up the timestamps
first_timestamp = time.time()
old_timestamp_1 = first_timestamp
old_timestamp_2 = first_timestamp
old_timestamp_3 = first_timestamp


## Initializing the variables
music = []
track1_note = 'C3'
track2_note = 'E3'
track3_note = 'G3'
intensity = 0.5
winning_status = 0.5
running = True


while running:

    ## Key Input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
        if event.type == JOYAXISMOTION:
            if event.axis == 1:
                intensity = (1 - event.value) / 2
            if event.axis == 3:
                winning_status = (1 - event.value) / 2

    ## Updating the tracks.
    curr_timestamp = time.time()

    if curr_timestamp - old_timestamp_1 >= bps():
        old_timestamp_1 = curr_timestamp
        duration = 1.
        pitch = next_note(0, track1_note, track2_note, track3_note)
        track1_note = pitch
        music.append(synth(pitches[pitch], duration=duration))

        print('intensity:', intensity, 'winning status:', winning_status)

    if curr_timestamp - old_timestamp_2 >= 2 * bps():
        old_timestamp_2 = curr_timestamp
        duration = 2.
        pitch = next_note(1, track1_note, track2_note, track3_note)
        track2_note = pitch
        music.append(synth(pitches[pitch], duration=duration))

        print('intensity:', intensity, 'winning status:', winning_status)

    if curr_timestamp - old_timestamp_3 >= 3*bps()/2:
        old_timestamp_3 = curr_timestamp
        duration = 1.3
        pitch = next_note(2, track1_note, track2_note, track3_note)
        track3_note = pitch
        music.append(synth(pitches[pitch], duration=duration))

        print('intensity:', intensity, 'winning status:', winning_status)


    if len(music) > 0:
        for note in music:
            # print(note)
            note.play(fade_ms=10)
            music.remove(note)

pg.mixer.quit()
pg.quit()