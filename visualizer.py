#!/usr/bin/env python3

import os, sys
import json, time, random, model
import signal_processing as sp
from housepy import log, config

MIN_STEPS = 10


def get_data():

    data = {}

    try:

        walks = model.fetch_walks(desc=False)

        notes = []
        v = 0
        ids = []
        for walk in walks:
            sequence = model.fetch_sequence(walk['id'])
            if len(sequence) < MIN_STEPS:
                continue
            for step in sequence:
                notes.append((step[0], v, 0 if step[1] == 'left' else 1))
            v += 1
            ids.append(walk['id'])

        # sort and normalize onsets
        notes.sort(key=lambda x: x[0])
        onsets = [note[0] for note in notes]
        onsets = sp.normalize(onsets)
        notes = [(onsets[i], note[1], note[2]) for (i, note) in enumerate(notes)]

        # print(notes)

        data['notes'] = notes
        data['walk_ids'] = ids

    except Exception as e:
        log.error(log.exc(e))
        return {}

    return json.dumps(data)

