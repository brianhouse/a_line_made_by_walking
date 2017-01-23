#!/usr/bin/env python3

import os, json, model, random, visualizer
from housepy import config, log, strings, server
from housepy import process as pc
from process import process_walk

pc.secure_pid(os.path.join(os.path.dirname(__file__), "run"))


class Home(server.Handler):

    def get(self, page=None, walk_id=None):
        log.info("Home.get %s" % page)
        if not len(page):
            return self.render("home.html")        
        if page == "walk":            
            if len(walk_id) and walk_id == "c":
                walk_id = random.choice(config['walk_ids'])
            if not type(walk_id) == int and not len(walk_id):
                walk_id = None
            return self.render("walk.html", sequence=json.dumps(model.fetch_sequence(walk_id)), ref_id=walk_id) 
        if page == "choose":
            return self.render("choose.html", walks=model.fetch_walks()) 
        if page in ["prepare", "route", "map", "thanks", "orientation", "background"]:
            return self.render("%s.html" % page)
        return self.not_found()

    def post(self, nop=None, nop2=None):
        log.info("Home.post")
        try:
            data = json.loads(self.get_argument('walk_data'))
            # log.debug(data)
        except Exception as e:
            return self.error(log.exc(e))
        if not len(data['accel_data']):
            return self.error("NO DATA")
        walk_id = model.insert_walk(data)
        log.info("Processing data...")
        try:    
            process_walk(walk_id)
        except Exception as e:
            return self.error("Could not process: %s" % log.exc(e))
        log.info("--> done")
        return self.text("OK")


class Sequence(server.Handler):

    def get(self, walk_id=None):
        log.info("Sequence.get %s" % walk_id)
        data = model.fetch_squence(walk_id)
        return self.json(data)


class Visualizer(server.Handler):

    def get(self, page=None):
        log.info("Visualizer.get %s" % page)
        data = visualizer.get_data()
        return self.render("vis.html", v=random.randint(0, 1000000), data=data)


def main():
    handlers = [
        (r"/sequence/?([^/]*)", Sequence),   
         (r"/visualize/?([^/]*)", Visualizer),     
        (r"/?([^/]*)/?([^/]*)", Home),
    ]
    server.start(handlers)      
                     
if __name__ == "__main__":
    main()
