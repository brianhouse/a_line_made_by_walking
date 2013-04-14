#!/usr/bin/env python

import os, time, json, datetime, model
from housepy import page, log
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
    walk_id = model.insert_walk(data)
    log.info("Processing data...")
    try:    
        process_walk(data['accel_data'], walk_id)
    except Exception as e:
        page.error("Could not process: %s" % log.exc(e))
        exit()
    log.info("--> done")
    page.text("OK")
else:
    page.render("home.html", {'walks': model.fetch_walks()})
