#!/usr/bin/env python3

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import json, time, random, model
import signal_processing as sp
from housepy import log, config, drawing

walks = model.fetch_walks()
walks = [walk for walk in walks if walk['id'] >= config['walk_id']]

notes = []
v = 0
for walk in walks:
    for step in model.fetch_sequence(walk['id']):
        notes.append((step[0], v, 0 if step[1] == 'left' else 1))
    v += 1

# sort and normalize onsets
notes.sort(key=lambda x: x[0])
onsets = [note[0] for note in notes]
onsets = sp.normalize(onsets)
notes = [(onsets[i], note[1], note[2]) for (i, note) in enumerate(notes)]

# print(notes)

margin = 50
ctx = drawing.Context(30000, 500, relative=True, flip=True, margin=margin, background=(252, 245, 216))
ctx.line(0.0 - (2.0 / ctx.width), 0.0, 1.0, 0.0, thickness=5)
ctx.line(0.0, 0.0 - (2.0 / ctx.height), 0.0, 1.0, thickness=5)

for note in notes:
    x = note[0]
    y = note[1] / float(v)
    size = 10.0
    x += 50.0 / ctx.width
    y += 50.0 / ctx.height
    y += 15.0 / ctx.height if note[2] == 1 else 0.0
    x += (random.random() * 5.0) / ctx.width
    y += (random.random() * 5.0) / ctx.height
    fill = (252, 245, 216) if note[2] else (0., 0., 0.)
    ctx.arc(x, y, size / ctx.width, size / ctx.height, fill=fill, thickness=3.0)


ctx.show()
ctx.image.save("charts/vis_%s.png" % int(time.time()), "PNG")


"""
x-axis is time
could also be place, as in how far on the track

"""