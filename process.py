#!/usr/bin/env python3

import sys, json, time, model
import numpy as np
import signal_processing as sp
from housepy import log, config

def process_walk(walk_id, force=False):

    if not model.process_check(walk_id):
        log.error("Walk %s already processed" % walk_id)        
        if force:
            log.info("--> forcing...")
            model.remove_sequence(walk_id)
        else:
            return
    log.info("Processing walk %s" % walk_id)

    data = model.fetch_accels(walk_id)
    data = [(reading['t'], reading['x'], reading['y'], reading['z']) for reading in data]
    # log.debug(data)

    # let's sample every millisecond, so the time of the last reading is how many samples we need
    data = np.array(data)
    # log.debug(data)
    ts = data[:,0]
    total_samples = int(ts[-1])

    if total_samples < 3500 + 5000: # need at least 5s of data
        log.info("No footsteps detected")
        return

    # resample the values
    xs = sp.resample(ts, data[:,1], total_samples)
    ys = sp.resample(ts, data[:,2], total_samples)
    zs = sp.resample(ts, data[:,3], total_samples)

    # skip 0.5s for accelerometer startup, and 3s for phone out of pocket at end
    skipin, skipout = 500, 3000
    xs = xs[skipin:-skipout]
    ys = ys[skipin:-skipout]
    zs = zs[skipin:-skipout]
    total_samples -= (skipin + skipout)

    log.info("TOTAL SAMPLES %s (%fs)" % (total_samples, (total_samples / 1000.0)))

    # get RMS
    # assume up and down is never important
    ds = np.sqrt((np.power(xs, 2) + np.power(zs, 2)) / 2)   

    # normalize the other values to a given range (this is gs, I believe), just for display
    MIN = -10.0
    MAX = 10.0
    xs = (xs - MIN) / (MAX - MIN)
    ys = (ys - MIN) / (MAX - MIN)
    zs = (zs - MIN) / (MAX - MIN)

    # process the RMS
    ds = sp.smooth(ds, 1000)
    ds = sp.normalize(ds)

    # detect peaks
    # lookahead should be the minimum time of a step, maybe .3s, 300ms
    peaks, valleys = sp.detect_peaks(ds, lookahead=300, delta=0.10)
    if len(peaks) and peaks[0][0] == 0:
        peaks = peaks[1:]
    peaks = np.array(peaks)
    valleys = np.array(valleys)[1:] # toss the first valley (always false)
    log.info("PEAKS %s" % len(peaks))

    if not len(peaks):
        log.info("No footsteps detected")
        return

    rights = peaks[:,0]
    lefts = []
    for r in range(len(rights)):
        if r == 0:
            continue
        lefts.append((rights[r-1] + rights[r]) / 2)

    # autocorrelate to verify

    # # adjust the start time to the first step
    # start = int(np.min([np.min(peaks[:,0]), np.min(valleys[:,0])]))
    # log.debug("START %s" % start)
    # xs = xs[start:]
    # ys = ys[start:]
    # zs = zs[start:]
    # ds = ds[start:]
    # peaks = [(peak[0] - start, peak[1]) for peak in peaks]
    # valleys = [(valley[0] - start, valley[1]) for valley in valleys]
    # total_samples -= start

    # save
    log.info("Saving sequence (%s)..." % walk_id)
    sequence = []
    for r, right in enumerate(rights):
        sequence.append((int(right), 'right'))
    for l, left in enumerate(lefts):
        sequence.append((int(left), 'left'))
    sequence.sort(key=lambda s: s[0])
    model.insert_sequence(walk_id, sequence)

    plot(walk_id, xs, ys, zs, ds, peaks, rights, lefts, total_samples)


def plot(walk_id, xs, ys, zs, ds, peaks, rights, lefts, total_samples):

    try:
        from housepy import drawing
    except:
        log.error("Can't draw")
        return

    # plot
    ctx = drawing.Context(5000, 600, relative=True, flip=True)
    ctx.line(200.0 / total_samples, 0.5, 350.0 / total_samples, 0.5, thickness=10.0)
    ctx.line([(float(i) / total_samples, x) for (i, x) in enumerate(xs)], stroke=(1., 0., 0., 0.5))
    ctx.line([(float(i) / total_samples, y) for (i, y) in enumerate(ys)], stroke=(0., 1., 0., 0.5))
    ctx.line([(float(i) / total_samples, z) for (i, z) in enumerate(zs)], stroke=(0., 0., 1., 0.5))
    ctx.line([(float(i) / total_samples, d) for (i, d) in enumerate(ds)], stroke=(0., 0., 0.), thickness=2.0)
    for peak in peaks:
        x, y = peak
        x = float(x) / total_samples
        ctx.arc(x, y, (10.0 / ctx.width), (10.0 / ctx.height), fill=(1., 0., 0.), thickness=0.0)
    for right in rights:
        x = float(right) / total_samples
        ctx.arc(x, 0.1, (10.0 / ctx.width), (10.0 / ctx.height), fill=(1., 0., 0.), thickness=0.0)        
    for left in lefts:
        x = float(left) / total_samples
        ctx.arc(x, 0.1, (10.0 / ctx.width), (10.0 / ctx.height), fill=(0., 0., 1.), thickness=0.0)        
    ctx.output("charts/steps_%s_%s.png" % (walk_id, int(time.time())))


if __name__ == "__main__":
    walk_id = sys.argv[1]
    force = True if len(sys.argv) > 2 and sys.argv[2][0] == "f" else False
    if walk_id == "all":
        walks = model.fetch_walks()
        log.info("Total walks: %s" % len(walks))
        for walk in walks:
            process_walk(walk['id'], force)
    else:
        process_walk(walk_id, force)


