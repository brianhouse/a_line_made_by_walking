#!/usr/bin/env python

import sqlite3, json
from housepy import config, log

connection = sqlite3.connect("walk_data.db")
connection.row_factory = sqlite3.Row
db = connection.cursor()

def init():
    try:
        db.execute("CREATE TABLE walks (start_time INT, duration INT, user TEXT)")
        db.execute("CREATE TABLE geo_data (walk_id INT, t INT, lat REAL, lng REAL)")
        db.execute("CREATE TABLE accel_data (walk_id INT, t INT, x REAL, y REAL, z REAL)")
        db.execute("CREATE TABLE sequence (walk_id INT, t INT, foot TEXT)")
    except Exception as e:
        if not "already exists" in e.message:
            raise e
    connection.commit()
init()

def insert_walk(walk):
    db.execute("INSERT INTO walks (start_time, duration, user) VALUES (?, ?, ?)", (walk['start_time'], walk['duration'], walk['user']))
    walk_id = db.lastrowid    
    for gd in walk['geo_data']:
        db.execute("INSERT INTO geo_data (walk_id, t, lat, lng) VALUES (?, ?, ?, ?)", (walk_id, gd[0], gd[1], gd[2]))
    for ad in walk['accel_data']:
        db.execute("INSERT INTO accel_data (walk_id, t, x, y, z) VALUES (?, ?, ?, ?, ?)", (walk_id, ad[0], ad[1], ad[2], ad[3]))
    connection.commit()
    return walk_id

def insert_sequence(walk_id, sequence):
    for step in sequence:
        db.execute("INSERT INTO sequence (walk_id, t, foot) VALUES (?, ?, ?)", (walk_id, sequence[0], sequence[1]))
    connection.commit()

def fetch_walks():
    db.execute("SELECT * FROM walks")
    rows = db.fetchall()
    return rows

def fetch_sequence(walk_id):
    db.execute("SELECT * FROM sequence WHERE walk_id=?", walk_id)
    rows = db.fetchall()
    return rows


