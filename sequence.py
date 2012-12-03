#!/usr/bin/env python

import os, time, json, datetime
from housepy import config
from housepy import page, log
from housepy.crashdb import CrashDB
from process import process_walk



db = CrashDB("sequence_data.json")    
if 'index' not in page.form or not len(page.form['index']):
    page.json([])
else:
    try:
        index = page.form['index']
        data = db[index]
        log.debug(data)
        page.json(data)
    except Exception as e:
        page.error("Index does not exist (%s)" % log.exc(e))

db.close()
