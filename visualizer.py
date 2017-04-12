#!/usr/bin/env python3

import os, sys
import json, time, random, model
import signal_processing as sp
from housepy import log, config


def get_data(hidden=False):

    log.debug("HIDDEN %s" % hidden)

    data = {}

    try:

        walks = model.fetch_walks(hidden=hidden)

        notes = []
        v = 0
        ids = []
        for walk in walks:
            sequence = model.fetch_sequence(walk['id'])
            if len(sequence) < config['min_steps']:
                continue
            for step in sequence:#[:config['max_steps']]:
                notes.append((step[0], v, 0 if step[1] == 'left' else 1))
            v += 1
            ids.append(walk['id'])

        # sort and normalize onsets
        notes.sort(key=lambda x: x[0])
        onsets = [note[0] for note in notes]
        onsets = sp.normalize(onsets)
        notes = [(onsets[i], note[1], note[2]) for (i, note) in enumerate(notes)]

        log.info("NOTES %s" % len(notes))

        data['notes'] = notes
        data['walk_ids'] = ids

    except Exception as e:
        log.error(log.exc(e))
        return {}

    return json.dumps(data)

