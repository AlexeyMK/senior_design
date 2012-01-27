"""
The server that mechanical turkers are using
"""

import cherrypy
from jinja2 import Environment, FileSystemLoader
import random


env = Environment(loader=FileSystemLoader('templates'))


class MarketplacePage:
    
  _cp_config = {'tools.sessions.on': True}

  @cherrypy.expose
  def entry_point(self, turker_id=1):
    # save turker's id
    cherrypy.session['turker'] = turker_id
    
    return env.get_template('intro.html').render()

  @cherrypy.expose
  def receive_offer(self):
    amount = random.randint(0,10) * 10
    cherrypy.session['amount'] = amount
    
    return env.get_template('offer.html').render(amount=amount)

  def accept(self):
    return "Great, congrats, thanks for playing!"
  accept.exposed = True

  def reject(self):
    return "fair enough, thanks for playing!"
  reject.exposed = True

import os.path
localconf = os.path.join(os.path.dirname(__file__), 'local.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(MarketplacePage(), config=localconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(MarketplacePage(), config=localconf)
