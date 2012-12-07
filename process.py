#!/usr/bin/env python

import sys, json, time
import numpy as np
from housepy import log, config, science
from housepy import signal_processing as sp
from housepy.crashdb import CrashDB, CrashDBError

def process_walk(data):

    # store data
    index = data['start_time']
    duration = data['duration']
    geo_data = data['geo_data']

    # get data    
    data = np.array(data['accel_data'])
    if not len(data):
        log.info("--> no acceleration data")
        return
    ts = data[:,0] - np.min(data[:,0]) # make ms timestamps relative

    # let's sample every millisecond, so the time of the last reading is how many samples we need
    total_samples = ts[-1]
    log.info("TOTAL SAMPLES %s (%fs)" % (total_samples, (total_samples / 1000.0)))

    # resample the values
    xs = sp.resample(ts, data[:,1], total_samples)
    ys = sp.resample(ts, data[:,2], total_samples)
    zs = sp.resample(ts, data[:,3], total_samples)

    # skip 3 seconds for putting the phone in the pocket
    skip = 3000
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
    log.info("Saving sequence (%s)..." % index)
    db = CrashDB("sequence_data.json")
    ## will have to change this to real right/lefts
    sequence = []
    for p, peak in enumerate(peaks):
        foot = 'left' if p % 2 == 0 else 'right'
        sequence.append((peak[0], foot))
    db[index] = {'steps': sequence, 'geo_data': geo_data, 'start_time': index, 'duration': duration}
    db.close()

    plot(index, xs, ys, zs, ds, peaks, valleys, total_samples)


def plot(index, xs, ys, zs, ds, peaks, valleys, total_samples):

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
    ctx.image.save("charts/%s_%s.png" % (index, int(time.time())), "PNG")
    if __name__ == "__main__":
        ctx.show()


if __name__ == "__main__":
    index = sys.argv[1]
    log.info(index)
    db = CrashDB("walk_data.json")
    try:
        data = db[index]
    except CrashDBError as e:
        log.error(e)        
        db.close()
    else:
        db.close()    
        process_walk(data)


# ## other ideas

# # find 'jerks'
# dr = science.derivative(ds)
# dr = sp.normalize(dr)

