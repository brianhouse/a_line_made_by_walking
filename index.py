#!/usr/bin/env python

import os, time, json, datetime
from housepy import page, log
from housepy.crashdb import CrashDB
from process import process_walk


db = CrashDB("walk_data.json")

if page.method == 'POST':
    log.info("Received walk data...")
    data = json.loads(page.form['walk_data'])  
    index = int(time.time())
    db[index] = data
    process_walk(data)
    page.text("OK")
else:
    options = {}
    for timestamp in db:
        options[timestamp] = datetime.datetime.fromtimestamp(float(timestamp))
    page.render("home.html", {'options': options})

db.close()