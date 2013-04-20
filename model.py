#!/usr/bin/env python

import sqlite3, json
from housepy import config, log

connection = sqlite3.connect("walk_data.db")
connection.row_factory = sqlite3.Row
db = connection.cursor()
# what's the danger of the connection closing accidentally? I dont think much
# and tornado is single threaded, so commits should be fine

def init():
    try:
        db.execute("CREATE TABLE walks (id INTEGER PRIMARY KEY, start_time INTEGER, duration INTEGER)")
        db.execute("CREATE TABLE geo_data (walk_id INTEGER, t INTEGER, lat REAL, lng REAL)")
        db.execute("CREATE INDEX geo_data_walk_id ON geo_data(walk_id)")
        db.execute("CREATE TABLE accel_data (walk_id INTEGER, t INTEGER, x REAL, y REAL, z REAL)")
        db.execute("CREATE INDEX accel_data_walk_id ON accel_data(walk_id)")
        db.execute("CREATE TABLE sequence (walk_id INTEGER, t INTEGER, foot TEXT)")
        db.execute("CREATE INDEX sequence_walk_id ON sequence(walk_id)")
    except Exception as e:
        if not "already exists" in e.message:
            raise e
    connection.commit()
init()

def insert_walk(walk):
    try:
        db.execute("INSERT INTO walks (start_time, duration) VALUES (?, ?)", (walk['start_time'], walk['duration']))
        walk_id = db.lastrowid    
        for gd in walk['geo_data']:
            db.execute("INSERT INTO geo_data (walk_id, t, lat, lng) VALUES (?, ?, ?, ?)", (walk_id, gd[0], gd[1], gd[2]))
        for ad in walk['accel_data']:
            db.execute("INSERT INTO accel_data (walk_id, t, x, y, z) VALUES (?, ?, ?, ?, ?)", (walk_id, ad[0], ad[1], ad[2], ad[3]))
    except Exception as e:
        log.error(log.exc(e))
        return None
    connection.commit()
    return walk_id

def insert_sequence(walk_id, sequence):
    try:
        for step in sequence:
            db.execute("INSERT INTO sequence (walk_id, t, foot) VALUES (?, ?, ?)", (walk_id, int(step[0]), step[1]))
    except Exception as e:
        log.error(log.exc(e))
        return None
    connection.commit()

def fetch_walks():
    db.execute("SELECT * FROM walks")
    walks = db.fetchall()
    for w, walk in enumerate(walks):
        walk = dict(walk)
        db.execute("SELECT * FROM geo_data WHERE walk_id=?", (walk['id'],))
        walk['geo_data'] = [dict(gd) for gd in db.fetchall()]
        log.debug(walk['geo_data'])
        walks[w] = walk
    return walks

def fetch_sequence(walk_id):
    db.execute("SELECT * FROM sequence WHERE walk_id=?", (walk_id,))
    sequence = [(step['t'], step['foot']) for step in db.fetchall()]
    return sequence

def fetch_accels(walk_id):
    db.execute("SELECT * FROM accel_data WHERE walk_id=?", (walk_id,))
    rows = [dict(reading) for reading in db.fetchall()]
    return rows

def process_check(walk_id):
    db.execute("SELECT * FROM sequence WHERE walk_id=?", (walk_id,))
    return len(db.fetchall()) == 0
    


