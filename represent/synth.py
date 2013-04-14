#!/usr/bin/env python

import json, time
from braid import *
from housepy import log, config
from housepy.crashdb import CrashDB
import housepy.signal_processing as sp

# collect notes
db = CrashDB("sequence_data.json")
notes = []
v = 0
voices = []
for index, walk in db.items():
    voices.append(Voice(v + 1))
    for step in walk['steps']:
        notes.append((step[0], v, 0 if step[1] == 'left' else 1))
    v += 1
db.close()        

# sort and normalize onsets
notes.sort(key=lambda x: x[0])
onsets = [note[0] for note in notes]
onsets = sp.normalize(onsets)
notes = [(onsets[i], note[1], note[2]) for (i, note) in enumerate(notes)]


# define voices
# for index in db:

for voice in voices:
    voice.synth = 'cycle'
    voice.attack = 350
    voice.sustain = 350
    voice.decay = 600
    voice.reverb = 0.7, 0.3, 0.25, 0.5, 0.0
    # voice.chord = C3

steps = [   (C3, D3),
            (G3, A3),
            (D4, E4),
            (A4, B4)
            ]    

DURATION = 20 * 60.0

start_time = time.time()
t = 0.0
for n, note in enumerate(notes):
    v = note[1]
    # step = v * 2
    # step = v * 2 if note[2] else (v * 2) + 1
    step = steps[v][note[2]]
    voices[v].pan = 1.0 if note[2] else 0.0
    voices[v].play(step)
    if n == len(notes) - 1:
        continue
    while t < notes[n+1][0] * DURATION:
        time.sleep(0.01)
        t = time.time() - start_time




