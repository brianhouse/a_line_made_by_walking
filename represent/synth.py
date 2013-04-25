#!/usr/bin/env python3

import os, sys, time, json
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import model
import signal_processing as sp
from braid import *
from braid.voice.msp_swerve import MspSwerve


MIN_WALK_ID = 26    # python3 cant use housepy

walks = model.fetch_walks()
walks = [walk for walk in walks if walk['id'] >= MIN_WALK_ID]

# collect notes
notes = []
v = 0
voices = []
for walk in walks:
    voices.append(MspSwerve(v + 1))
    for step in model.fetch_sequence(walk['id']):
        notes.append((step[0], v, 0 if step[1] == 'left' else 1))
    v += 1   

# sort and normalize onsets
notes.sort(key=lambda x: x[0])
onsets = [note[0] for note in notes]
onsets = sp.normalize(onsets)
notes = [(onsets[i], note[1], note[2]) for (i, note) in enumerate(notes)]


for voice in voices:
    # voice.synth = 'cycle'
    voice.synth = 'rect'
    voice.attack = 350
    # voice.sustain = 350
    voice.sustain = 2000
    voice.decay = 600
    voice.reverb = 0.5, 0.5, 0.45, 0.5, 0.0
    # voice.chord = C3

steps = [   (C3, D3),
            (G3, A3),
            (D4, E4),
            (A4, B4),
            (E5, F5),
            (G5, A5)
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
    voices[v].play(step, 1.0)
    if n == len(notes) - 1:
        continue
    while t < notes[n+1][0] * DURATION:
        time.sleep(0.01)
        t = time.time() - start_time




