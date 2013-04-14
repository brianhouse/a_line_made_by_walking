import cgi, os, filters, sys
import filters, strings
import cgitb
cgitb.enable()  # detailed errors on fail
import jinja2, net
from config import config
from log import log

form = {}
if 'REQUEST_METHOD' in os.environ:
    body = sys.stdin.read()    
    method = os.environ['REQUEST_METHOD'] if 'REQUEST_METHOD' in os.environ else None
    uri = os.environ['REQUEST_URI'] if 'REQUEST_URI' in os.environ else None
    fs = cgi.FieldStorage(keep_blank_values=True)
    for k in fs.keys():
        form[k] = fs[k].value
    try:
        post_vars = net.urldecode(body)
    except Exception:
        pass
    else:
        form.update(post_vars)
    log.info("----- %s %s ---------------------------------------------------------" % (method, uri))        
    log.info("REQUEST_VARS: %s" % form)
    # log.info("REQUEST_BODY: %s" % body)
else:
    method = None

class render_jinja:

    def __init__(self, *a, **kwargs):
        extensions = kwargs.pop('extensions', [])
        globals = kwargs.pop('globals', {})

        from jinja2 import Environment, FileSystemLoader
        self._lookup = Environment(loader=FileSystemLoader(*a, **kwargs), extensions=extensions)
        self._lookup.globals.update(globals)
        
    def __getitem__(self, name):
        t = self._lookup.get_template(name)
        return t.render

def render(template_name, template_values=None, **kwargs):
    if type(template_values) == dict:
        template_values.update(kwargs)
    else:
        template_values = kwargs
    log.info("TEMPLATE %s" % (template_name))
    for key in config:      
        if type(config[key]) is list and 0 in config[key] and type(config[key][0]) is dict:
            for param in config[key][0]:
                template_values[key + "_" + param] = config[key][0][param]
        else:
            template_values[key] = config[key]              
    template_values['template_name'] = template_name    
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates/"))
    if not os.path.isdir(template_dir):
        os.mkdir(template_dir)    
    renderer = render_jinja(template_dir)
    renderer._lookup.filters.update(filters.filters)
    output = (renderer[template_name](template_values)).encode('utf-8')
    suffix = strings.suffix('.', template_name)
    if suffix == "html":
        html(output)
    else:
        text(output)    
    
def json(data, filename=None):
    import json as jsonlib
    try:
        import numpy as np
    except Exception:    
        output = jsonlib.dumps(data, indent=4, default=lambda obj: str(obj))               
    else:    
        output = jsonlib.dumps(data, indent=4, default=lambda obj: str(obj) if type(obj) != np.ndarray else list(obj))
    print("Content-Type: text/plain\n")
    if filename:
        print("Content-Disposition: attachment; filename=%s\n" % filename)
    print(output)
    log.info("200 text/plain (JSON)")

    
def xml(xml):    
    print("Content-Type: application/xml\n")
    print(xml)
    log.info("200: application/xml")                            

def html(html):
    print("Content-Type: text/html\n")
    print(html)    
    log.info("200: text/html")                
    
def text(string):
    print("Content-Type: text/plain\n")
    print(string)
    log.info("200: text/plain")            

def csv(string, filename):
    print("Content-Type: text/csv")
    print("Content-Disposition: attachment; filename=%s\n" % filename)
    print(string)
    log.info("200: text/csv")    
    
def file(filename):
    print("Content-Type: application/octet-stream")
    print("Content-Disposition: attachment; filename=%s" % filename)
    # print("Content-Transfer-Encoding: binary")
    # print("Cache-Control: no-cache")
    # print("Pragma: no-cache")    
    print("Content-Length: %s\n" % os.path.getsize(filename))    
    print(open(filename, 'r').read())
    log.info("200: application/octet-stream (%s)" % filename)        
    
def image(image):
    print("Content-Type: image/png\n")
    print("Expires Thu, 15 Apr 2050 20:00:00 GMT")
    print(image)
    log.info("200: image/png")            

def temp_image(image):
    print("Content-Type: image/png\n")     
    print("Cache-Control: no-cache")
    print(image)
    log.info("200: image/png (temporary)")            

def error(message):
    print("Status: 400 Bad Request\n")
    print("400: %s" % message)
    log.error("400: %s" % message)    

def not_found():
    print("Status: 404 Not Found\n")
    print("404")
    log.error("404: Page not found")    
    
def redirect(url):
    print("Status: 303 See Other")    
    print("Location: %s\n" % url)
    print("Redirecting to %s" % url)
    log.info("303: Redirecting to %s" % url)          
    
def refresh():
    redirect(os.environ['REQUEST_URI'])

def info():
    import strings
    output = []
    for key in os.environ.keys():
        output.append("%s: %s" % (key, os.environ[key]))
    output = "\n".join(output)
    log.info(output)
    output = strings.nl2br(output)
    html(output)
