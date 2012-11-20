#!/usr/bin/env python

import os, time, json
from housepy import page, log
from housepy.crashdb import CrashDB

if page.method == 'POST':
    log.info("Received walk data...")
    try:
        db = CrashDB("walk_data.json")
        data = json.loads(page.form['walk_data'])
        db[int(time.time())] = data
        db.close()
    except Exception as e:
        try:
            db.close()
        except:
            pass
        page.error(e)
        exit()    
    page.text("OK")
else:
    page.render("home.html", {})
