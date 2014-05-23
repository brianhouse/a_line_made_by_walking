#!/usr/bin/env python3

import os, sys, time
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import model
import numpy as np
from housepy import config, log, drawing, geo, util

MIN_STEPS = 50

walk_data = model.fetch_walks(desc=False)
# walk_data = [walk for walk in walks if walk['id'] >= config['walk_id']]

walks = []
for walk in walk_data:
    sequence = model.fetch_sequence(walk['id'])
    if len(sequence) < MIN_STEPS:
        continue
    walks.append(walk)


LON = 0
LAT = 1
X = 2
Y = 3

all_points = []
for walk in walks:
    points = model.fetch_geo(walk['id'])
    points = np.array([(point['lng'], point['lat'], None, None) for point in points])
    for point in points:
        point[X], point[Y] = geo.project((point[LON], point[LAT]))
    walk['points'] = points
    all_points.extend(points)
all_points = np.array(all_points)

max_x = np.max(all_points[:,X])
min_x = np.min(all_points[:,X])
max_y = np.max(all_points[:,Y])
min_y = np.min(all_points[:,Y])

width = float(abs(max_x - min_x))
height = float(abs(max_y - min_y))
ratio = width / height

print(ratio)
    
points = list(points)
for walk in walks:
    for point in walk['points']:
        point[X] = util.scale(point[X], min_x, max_x)
        point[Y] = util.scale(point[Y], min_y, max_y)



ctx = drawing.Context(1000, int(1000.0/ratio), relative=True, flip=True, hsv=True, margin=20, background=(252/256, 245/256, 216/256))

for w, walk in enumerate(walks):
    c = float(w) / len(walks)
    points = [(point[X], point[Y]) for point in walk['points']]
    # ctx.line(points, thickness=3.0, stroke=(0.55, 1.0, c))
    # ctx.line(points, thickness=3.0, stroke=(0.55, 0.0, c))    
    # ctx.line(points, thickness=5.0, stroke=(0.55, 1.0, 0.7, 0.4))
    ctx.line(points, thickness=5.0, stroke=(0.55, 0.0, 0.0, 0.4))
      
ctx.output("charts/geo_%s.png" % int(time.time()))



