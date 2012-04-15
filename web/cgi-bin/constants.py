MAPGEN_PATH = "/home/mtadd/src/mapgen"
TEMPLATE_PATH = "/home/mtadd/src/mapgen/web/wsgi/templates"
import cgitb
cgitb.enable()
import sys
sys.stderr = sys.stdout
sys.path.insert(0,MAPGEN_PATH)

_environment = None

def environment():
   global _environment
   if _environment is None:
      from jinja2 import Environment, FileSystemLoader
      _environment = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
   return _environment

def render_template(template, **kwargs):
   print 'Content-type: text/html'
   print
   print environment().get_template(template).render(**kwargs)
