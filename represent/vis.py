#!/usr/bin/env python

import json, time, random
from housepy import log, config, drawing
from housepy.crashdb import CrashDB
import housepy.signal_processing as sp

# collect notes
db = CrashDB("sequence_data.json")
notes = []
v = 0
for index, walk in db.items():
    for step in walk['steps']:
        notes.append((step[0], v, 0 if step[1] == 'left' else 1))
    v += 1
db.close()        

# sort and normalize onsets
notes.sort(key=lambda x: x[0])
onsets = [note[0] for note in notes]
onsets = sp.normalize(onsets)
notes = [(onsets[i], note[1], note[2]) for (i, note) in enumerate(notes)]

print notes

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
ctx.image.save("charts/walk_%s.png" % int(time.time()), "PNG")


"""
x-axis is time
could also be place, as in how far on the track

"""