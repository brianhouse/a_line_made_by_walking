#!/usr/bin/env python

import sys, json, time, model
import numpy as np
import signal_processing as sp
from housepy import log, config

def process_walk(walk_id):

    if not model.process_check(walk_id):
        log.error("Walk already processed")
        return

    data = model.fetch_accels(walk_id)
    data = [(reading['t'], reading['x'], reading['y'], reading['z']) for reading in data]
    # log.debug(data)

    # let's sample every millisecond, so the time of the last reading is how many samples we need
    data = np.array(data)
    # log.debug(data)
    ts = data[:,0]
    total_samples = ts[-1]
    log.info("TOTAL SAMPLES %s (%fs)" % (total_samples, (total_samples / 1000.0)))

    # resample the values
    xs = sp.resample(ts, data[:,1], total_samples)
    ys = sp.resample(ts, data[:,2], total_samples)
    zs = sp.resample(ts, data[:,3], total_samples)

    # skip 0.5s for intro
    skip = 500
    xs = xs[skip:]
    ys = ys[skip:]
    zs = zs[skip:]
    total_samples -= skip


    # # for testing
    # log.debug(total_samples)
    # xs = xs[(30 * 1000):(40 * 1000)]
    # ys = ys[(30 * 1000):(40 * 1000)]
    # zs = zs[(30 * 1000):(40 * 1000)]
    # total_samples = len(xs)
    # log.debug(total_samples)


    # get 3d vector
    ds = np.sqrt(np.power(xs, 2) + np.power(ys, 2) + np.power(zs, 2))

    # normalize the values to a given range (this is gs, I believe)
    MIN = -20.0
    MAX = 20.0
    xs = (xs - MIN) / (MAX - MIN)
    ys = (ys - MIN) / (MAX - MIN)
    zs = (zs - MIN) / (MAX - MIN)
    ds = (ds - MIN) / (MAX - MIN)

    # low-pass filter
    ds = sp.smooth(ds, 300)
    ds = sp.normalize(ds)
    av = np.average(ds)

    # detect peaks
    # lookahead should be the minimum time of a step, maybe .3s, 300ms
    peaks, valleys = sp.detect_peaks(ds, lookahead=150, delta=0.15)
    if peaks[0][0] == 0:
        peaks = peaks[1:]
    peaks = np.array(peaks)
    valleys = np.array(valleys)
    log.info("PEAKS %s" % len(peaks))
    log.info("VALLEYS %s" % len(valleys))

    if not (len(peaks) and len(valleys)):
        log.info("No footsteps detected")
        return

    peaks = valleys

    # start = np.min((np.min(peaks[:,0]), np.min(valleys[:,0])))
    start = np.min(peaks[:,0])
    log.debug("START %s" % start)
    xs = xs[start:]
    ys = ys[start:]
    zs = zs[start:]
    ds = ds[start:]
    peaks = [(peak[0] - start, peak[1]) for peak in peaks]
    valleys = [(valley[0] - start, valley[1]) for valley in valleys]
    total_samples -= start

    # print out
    log.info("Saving sequence (%s)..." % walk_id)
    ## will have to change this to real right/lefts
    sequence = []
    for p, peak in enumerate(peaks):
        foot = 'left' if p % 2 == 0 else 'right'
        sequence.append((peak[0], foot))
    model.insert_sequence(walk_id, sequence)

    plot(walk_id, xs, ys, zs, ds, peaks, valleys, total_samples)


def plot(walk_id, xs, ys, zs, ds, peaks, valleys, total_samples):

    try:
        from housepy import drawing
    except:
        log.error("Can't draw")
        return

    # plot
    ctx = drawing.Context(50000, 600, relative=True, flip=True)
    ctx.line(200.0 / total_samples, 0.5, 350.0 / total_samples, 0.5, thickness=10.0)
    ctx.line([(float(i) / total_samples, x) for (i, x) in enumerate(xs)], stroke=(1., 0., 0., 0.5))
    ctx.line([(float(i) / total_samples, y) for (i, y) in enumerate(ys)], stroke=(0., 1., 0., 0.5))
    ctx.line([(float(i) / total_samples, z) for (i, z) in enumerate(zs)], stroke=(0., 0., 1., 0.5))
    ctx.line([(float(i) / total_samples, d) for (i, d) in enumerate(ds)], stroke=(0., 0., 0.), thickness=2.0)
    for peak in peaks:
        x, y = peak
        x = float(x) / total_samples
        ctx.arc(x, y, (1.0 / ctx.width) * 10, (1.0 / ctx.height) * 10, fill=(1., 0., 0.), thickness=0.0)
    for valley in valleys:
        x, y = valley
        x = float(x) / total_samples
        ctx.arc(x, y, (1.0 / ctx.width) * 10, (1.0 / ctx.height) * 10, fill=(0., 0., 1.), thickness=0.0)
    ctx.image.save("charts/%s_%s.png" % (walk_id, int(time.time())), "PNG")
    if __name__ == "__main__":
        ctx.show()


if __name__ == "__main__":
    walk_id = sys.argv[1]
    process_walk(walk_id)




# ## other ideas

# # find 'jerks'
# dr = science.derivative(ds)
# dr = sp.normalize(dr)

