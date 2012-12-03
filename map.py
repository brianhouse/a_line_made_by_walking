#!/usr/bin/env python

import os, time, json, datetime
from housepy import page, log
from housepy.crashdb import CrashDB

db = CrashDB("sequence_data.json")    
options = {}
for timestamp in db:
    options[timestamp] = datetime.datetime.fromtimestamp(int(float(timestamp) / 1000.0))
db.close()        
page.render("map.html", {'options': options})
