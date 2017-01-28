#!/usr/bin/env python3

import sys, json, time, model, math
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

    # fetch data
    data = model.fetch_accels(walk_id)
    data = [(reading['t'], reading['x'], reading['y'], reading['z']) for reading in data]

    # let's sample every millisecond, so the time of the last reading is how many samples we need
    data = np.array(data)
    ts = data[:,0]
    total_samples = int(ts[-1])

    # need at least 10s of data
    # add 2000 for trimming at nd
    if total_samples < 10000 + 2000: 
        log.info("No footsteps detected (too short)")
        model.hide(walk_id)        
        return

    # resample the values
    xs = sp.resample(ts, data[:,1], total_samples)
    ys = sp.resample(ts, data[:,2], total_samples)
    zs = sp.resample(ts, data[:,3], total_samples)

    # skip for accelerometer startup and for phone out of pocket at end 
    skipin, skipout = 0, 2000
    xs = xs[skipin:-skipout]
    ys = ys[skipin:-skipout]
    zs = zs[skipin:-skipout]
    total_samples -= (skipin + skipout)
    log.info("TOTAL SAMPLES %s (%fs)" % (total_samples, (total_samples / 1000.0)))

    # get 3d magnitude (not RMS) -- orientation shouldnt matter
    ds = np.sqrt(np.power(xs, 2) + np.power(ys, 2) + np.power(zs, 2))    

    # prep the raw values for display
    # normalize the values to a given range  (this is Gs)
    MIN = -10.0
    MAX = 10.0
    xs = (xs - MIN) / (MAX - MIN)
    ys = (ys - MIN) / (MAX - MIN)
    zs = (zs - MIN) / (MAX - MIN)
    # smooth them
    xs = sp.smooth(xs, 300)
    ys = sp.smooth(ys, 300)
    zs = sp.smooth(zs, 300)

    # process the magnitude signal
    ds = sp.smooth(ds, 500)
    ds = np.clip(ds, -10.0, 10.0)   # limit the signal to +-10 Gs
    ds = sp.normalize(ds)
    ds = 1 - ds
    ds = sp.compress(ds, 3.0)
    ds = sp.normalize(ds)

    # detect peaks
    peaks, valleys = sp.detect_peaks(ds, lookahead=50, delta=0.10)
    peaks = np.array(peaks)
    valleys = np.array(valleys)
    log.info("PEAKS %s" % len(peaks))
    if not len(peaks):
        log.info("No footsteps detected")
        model.hide(walk_id)
        return

    # get foot separator line
    fxs = [int(peak[0]) for peak in peaks]
    fys = [peak[1] for peak in peaks]
    avs = np.average([peak[1] for peak in peaks])
    fys[0] = avs    # it's going to start with a peak, so we need to bring it up or down accordingly
    fxs.append(total_samples-1)
    fys.append(avs)
    fs = sp.resample(fxs, fys, total_samples)
    fs = sp.smooth(fs, 3000)

    # print out
    log.info("Saving sequence (%s)..." % walk_id)
    sequence = []
    for p, peak in enumerate(peaks):
        foot = 'right' if peak[1] > fs[int(peak[0])] else 'left'
        t = peak[0]
        t += 300   # turns out the peak hits just before the step
        sequence.append((t, foot))

    # fix triples
    for i in range(len(sequence) - 2):
        if sequence[i][1] == sequence[i+1][1] == sequence[i+2][1]:
            sequence[i+1] = (sequence[i+1][0], 'right') if sequence[i+1][1] == 'left' else (sequence[i+1][0], 'left')

    model.insert_sequence(walk_id, sequence)

    plot(walk_id, xs, ys, zs, ds, peaks, total_samples, fs)



def plot(walk_id, xs, ys, zs, ds, peaks, total_samples, fs):

    try:
        from housepy import drawing
    except:
        log.error("Can't draw")
        return

    # plot
    ctx = drawing.Context(5000, 600, relative=True, flip=True)
    ctx.line(200.0 / total_samples, 0.5, 350.0 / total_samples, 0.5, thickness=10.0)
    ctx.line([(float(i) / total_samples, x) for (i, x) in enumerate(xs)], stroke=(1., 0., 0., 1.0))# thickness=3.0)
    ctx.line([(float(i) / total_samples, y) for (i, y) in enumerate(ys)], stroke=(0., 1., 0., 1.0))#, thickness=3.0)
    ctx.line([(float(i) / total_samples, z) for (i, z) in enumerate(zs)], stroke=(0., 0., 1., 1.0))#, thickness=3.0)
    ctx.line([(float(i) / total_samples, d) for (i, d) in enumerate(ds)], stroke=(0., 0., 0.), thickness=3.0)
    ctx.line([(float(i) / total_samples, f) for (i, f) in enumerate(fs)], stroke=(1., 0., 1.), thickness=5.0)
    for peak in peaks:
        x, y = peak
        x = float(x) / total_samples
        ctx.arc(x, y, (10.0 / ctx.width), (10.0 / ctx.height), fill=(1., 0., 0.), thickness=0.0)
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


