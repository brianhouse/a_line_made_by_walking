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
    # log.debug("data: %s" % data)
    index = data['start_time']
    log.info("Saving data...")
    db = CrashDB("walk_data.json")
    db[index] = data
    db.close()
    log.info("Processing data...")
    try:    
        process_walk(data)
    except Exception as e:
        page.error("Could not process: %s" % e)
        exit()
    log.info("--> done")
    page.text("OK")
else:
    db = CrashDB("sequence_data.json")    
    options = {}
    for timestamp in db:
        options[timestamp] = datetime.datetime.fromtimestamp(float(timestamp) / 1000.0)
    db.close()        
    page.render("home.html", {'options': options})
