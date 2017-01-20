#!/usr/bin/env python3

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import json, time, random, model
import signal_processing as sp
from housepy import log, config, drawing

MIN_STEPS = 10

walks = model.fetch_walks(desc=False)
# walks = [walk for walk in walks if walk['id'] >= config['walk_id']]
# walks = [walk for walk in walks if walk['id'] == 1]

notes = []
v = 0
for walk in walks:
    sequence = model.fetch_sequence(walk['id'])
    if len(sequence) < MIN_STEPS:
        continue
    for step in sequence:
        notes.append((step[0], v, 0 if step[1] == 'left' else 1))
    v += 1

# notes = notes[:20]

# sort and normalize onsets
notes.sort(key=lambda x: x[0])
onsets = [note[0] for note in notes]
onsets = sp.normalize(onsets)
notes = [(onsets[i], note[1], note[2]) for (i, note) in enumerate(notes)]

# print(notes)

ctx = drawing.Context(30000, 2000, margin=75, background=(252/256, 245/256, 216/256))
ctx.line(0.0, 0.0, 1.0, 0.0, thickness=5)
ctx.line(0.0, 0.0, 0.0, 1.0, thickness=5)

for note in notes:
    x = note[0]
    y = note[1] / float(v)
    size = 20.0
    x += 50.0 / ctx.width
    y += 50.0 / ctx.height
    y += 15.0 / ctx.height if note[2] == 1 else 0.0
    x += (random.random() * 5.0) / ctx.width
    y += (random.random() * 5.0) / ctx.height
    fill = (252, 245, 216) if note[2] else (0., 0., 0.)
    ctx.arc(x, y, size / ctx.width, (size / ctx.height) * .5, fill=fill, thickness=3.0)


ctx.output("charts/vis_%s.png" % int(time.time()))


"""
x-axis is time
could also be place, as in how far on the track

"""