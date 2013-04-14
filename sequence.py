#!/usr/bin/env python

import os, time, json, datetime, model
from housepy import config
from housepy import page, log
from process import process_walk

if 'walk_id' not in page.form or not len(page.form['walk_id']):
    page.json([])
else:
    try:
        walk_id = page.form['walk_id']
        data = model.fetch_squence(walk_id)
        log.debug(data)
        page.json(data)
    except Exception as e:
        page.error("Index does not exist (%s)" % log.exc(e))
