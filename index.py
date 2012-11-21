#!/usr/bin/env python

import os, time, json, datetime
from housepy import page, log
from housepy.crashdb import CrashDB
from process import process_walk

if page.method == 'POST':
    log.info("Received walk data...")
    try:
        data = json.loads(page.form['walk_data'])  
    except Exception as e:
        page.error(e)
        exit()
    if not len(data):
        page.error("No data")
        exit()
    log.info("data: %s" % data)
    index = int(time.time())
    db = CrashDB("walk_data.json")
    db[index] = data
    db.close()
    process_walk(index)
    page.text("OK")
else:
    db = CrashDB("sequence_data.json")    
    options = {}
    for timestamp in db:
        options[timestamp] = datetime.datetime.fromtimestamp(float(timestamp))
    db.close()        
    page.render("home.html", {'options': options})