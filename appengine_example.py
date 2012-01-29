"""
Recipe for running a CherryPy-based server under the Google AppEngine.
There is actually nothing AppEngine-specific here - the key is setting up
the environment correctly by following the other steps.
"""
import cherrypy
import wsgiref.handlers

# application goes here ...
class Root:
    def index(self):
        return "Hello, CherryPy! version=",cherrypy.__version__
        
    index.exposed = True

#---------------------------------------------------------------------------
# Start the server under Google AppEngine
#---------------------------------------------------------------------------
app = cherrypy.tree.mount(Root(), "/")
wsgiref.handlers.CGIHandler().run(app)
