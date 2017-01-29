#!/usr/bin/env python3

import os, json, model, random, visualizer, base64, zlib
from housepy import config, log, strings, server, util
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
                walks = model.fetch_walks()
                if len(walks):
                    walk_id = random.choice(walks)['id']
                else:
                    walk_id = None
            elif not type(walk_id) == int and not len(walk_id):
                walk_id = None
            return self.render("walk.html", sequence=json.dumps(model.fetch_sequence(walk_id)), ref_id=walk_id) 
        if page == "walks":
            return self.render("walks.html", walks=model.fetch_walks(hidden=True))
        if page == "choose":
            return self.render("choose.html", walks=model.fetch_walks()) 
        if page in ["prepare", "route", "map", "thanks", "orientation", "background"]:
            return self.render("%s.html" % page)
        return self.not_found()

    def post(self, nop=None, nop2=None):
        log.info("Home.post")
        try:
            data = self.get_argument('walk_data')            
            data = base64.b64decode(data)
            data = zlib.decompress(data, -15)
            data = data.decode()
            data = json.loads(data)
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
        data = model.fetch_sequence(walk_id)
        return self.json(data, gzip=True)

    def post(self, nop=None):
        walk_id = self.get_argument('walk_id')
        show = self.get_argument('show')
        log.info("Sequence.post %s %s" % (walk_id, show))
        hidden = show == "false"
        model.hide(walk_id, hidden)
        return self.text("OK")


class Visualizer(server.Handler):

    def get(self, page=None):
        log.info("Visualizer.get %s" % page)
        hidden = True if page == "all" else False
        data = visualizer.get_data(hidden)
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
