"""
The server that mechanical turkers are using
TODO:
- actual accept/reject
- actual review
- no messing with amount offered.
- ensure it runs on GAE
- run on mturk playground
"""

import cherrypy
from jinja2 import Environment, FileSystemLoader
from google.appengine.api import memcache
from models import *

import wsgiref.handlers
import random
import sys

# patch sys memcache module locations to use GAE memcache
sys.modules['memcache'] = memcache
env = Environment(loader=FileSystemLoader('templates'))

def record_transaction(session, rating=None):
  trans = MarketTransaction(turker_id = session['turker'],
                   amount_offered_cents = session['amount'],
                   accepted_offer = session['accepted'],
                   rating_left = rating,
                   transaction_round = session['round'],
                   start_time = session['start_time'],
                   end_time = datetime.datetime.now(),
                   experiment = session['experiment']
        )
  trans.put() # save
  return trans

def render_for_experiment(page, experiment, **other_args):
  #TODO - headers, and general chrome/css
  other_args['conditions'] = experiment.conditions_json
  return env.get_template(page).render(**other_args)

class MarketplacePage:
  _cp_config = {'tools.sessions.on': True}

  @cherrypy.expose
  def intro(self, turker_id="1"):
    cherrypy.session['turker'] = turker_id

  # TODO: pick available experiment, set in session
    experiment = Experiment.all().filter('active =', True).get()
    if not experiment:
      return "Can't find an experiment for you, sorry"
    else:
      cherrypy.session['experiment'] = experiment
      return render_for_experiment('intro.html', experiment) 

  @cherrypy.expose
  def offer(self):
    if not 'round' in cherrypy.session:
      cherrypy.session['round'] = 0
    cherrypy.session['round'] += 1 # next round

    experiment = cherrypy.session['experiment']

    if cherrypy.session['round'] > experiment.num_rounds_per_subject:
      return render_for_experiment('end.html', experiment)
    else:
      #TODO - ask experiment to configure this randomness 
      amount = random.randint(0,10) * 10
      cherrypy.session['amount'] = amount
      cherrypy.session['start_time'] = datetime.datetime.now()
      return render_for_experiment('offer.html', experiment, amount=amount)
      
  @cherrypy.expose
  def review(self, accepted=True):
    #TODO - create MarketTransaction, write it, include link to 'next'
    cherrypy.session['accepted'] = accepted # TODO - get from form
    return render_for_experiment('review.html', cherrypy.session['experiment'])

  @cherrypy.expose
  def finished_round(self, rating=None):
    record_transaction(cherrypy.session, rating) 
    # Redirect back to offer
    return self.offer() 

# app engine specific:
# hack to make sessions work
# via http://appmecha.wordpress.com/2008/10/25/cherrypy-sessions-on-gae/
cf = {"/":{'tools.sessions.on':  True,
           'tools.sessions.storage_type': "memcached",
           'tools.sessions.servers': ['memcached://'],
           'tools.sessions.name': 'hello_gb_session_id',
           'tools.sessions.clean_thread': True,
           # ten minute session timeout, not sure if this works
           'tools.session.timeout': 10, 
            }}
app = cherrypy.tree.mount(MarketplacePage(), config=cf)
wsgiref.handlers.CGIHandler().run(app)
