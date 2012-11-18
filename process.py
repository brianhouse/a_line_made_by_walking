#!/usr/bin/env python

import sys, json
import numpy as np
from housepy import log, config, drawing, science
from housepy import signal_processing as sp

# load data
filename = sys.argv[1]
log.info("Reading %s" % filename)
with open(filename) as f:
    content = f.readlines()
data = []
for line in content:
    parts = line.strip().split(',')
    d = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
    data.append(d)
data = np.array(data)

data = data[:-5]

# the sampling between each analog pin is delayed ~= 11 ms, so this approximately corrects for it
# not as good as xbee sampling
t0s = data[:,0] - np.min(data[:,0])
t1s = t0s + 11
t2s = t1s + 11

# let's sample every millisecond, so the time of the last reading is how many samples we need
total_samples = t2s[-1]
log.info("TOTAL SAMPLES %s (%fs)" % (total_samples, (total_samples / 60.0)))

# resample the values
xs = sp.resample(t0s, data[:,1], total_samples)
ys = sp.resample(t1s, data[:,2], total_samples)
zs = sp.resample(t2s, data[:,3], total_samples)

MIN = 100.0
MAX = 400.0

# normalize the values to a given range
xs = (xs - MIN) / MAX
ys = (ys - MIN) / MAX
zs = (zs - MIN) / MAX

# get 3d vector
ds = np.sqrt(np.power(xs, 2) + np.power(ys, 2) + np.power(zs, 2))

# low-pass filter, invert, cut off everything above average
ds = sp.smooth(ds, 600)
ds = sp.normalize(ds)
ds = 1.0 - ds
av = np.average(ds)
ds -= av
ds *= ds >= 0
ds = sp.normalize(ds)

# detect peaks
peaks, valleys = sp.detect_peaks(ds, lookahead=50, delta=0.5)

print peaks


# plot
ctx = drawing.Context(5000, 600, relative=True, flip=True)
ctx.line([(float(i) / total_samples, x) for (i, x) in enumerate(xs)], stroke=(1., 0., 0., 0.3))
ctx.line([(float(i) / total_samples, y) for (i, y) in enumerate(ys)], stroke=(0., 1., 0., 0.3))
ctx.line([(float(i) / total_samples, z) for (i, z) in enumerate(zs)], stroke=(0., 0., 1., 0.3))
ctx.line([(float(i) / total_samples, d) for (i, d) in enumerate(ds)], stroke=(0., 0., 0.), thickness=2.0)
for peak in peaks:
    x, y = peak
    x = float(x) / total_samples
    ctx.arc(x, y, (1.0 / ctx.width) * 10, (1.0 / ctx.height) * 10, fill=(1., 0., 0.))
ctx.show()



# ## other ideas

# # find 'jerks'
# dr = science.derivative(ds)
# dr = sp.normalize(dr)





