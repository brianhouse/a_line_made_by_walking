#!/usr/bin/env python

import os, time, json, datetime
from housepy import page, log
from housepy.crashdb import CrashDB
from process import process_walk


db = CrashDB("sequence_data.json")    

try:
    index = page.form['index']
    data = db[index]
    page.json(data)
except Exception as e:
    page.error("Index does not exist (%s)" % log.exc(e))

db.close()
