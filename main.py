"""
NEXT:
- code that can pay turkers
  - in mturk.py,
  - query GQL for amt that turkers deserve
  - send appropriate bonuses
  TODO POSSIBILITIES for how to get rid of s~ thing:
  - extra libs in ../appengine/remote_api_shell
  - some setting in appengine/ext/remote_api/remote_api_stub.py

- get experiment creation down to: 
  I'd like to run an experiment with the following configs --> OK
    - creates AppEngine experiment, 
    - creates mturk task, 
    - emails when done
EVENTUALLY:
- way prettier (bootstrap?)
- save name in experiment name
- script that pushes and then hits the page once, so it doesn't have the first-hit hiccup
- smarter round update (IE, I know what page you should be on next, why aren't you there)
"""

import cherrypy
from cherrypy.lib.cptools import redirect
from jinja2 import Environment, FileSystemLoader
from google.appengine.api import memcache
from models import *

import wsgiref.handlers
import random
import sys, os
from urllib import urlencode

# patch sys memcache module locations to use GAE memcache
sys.modules['memcache'] = memcache
env = Environment(loader=FileSystemLoader('templates'))

def record_transaction(session, rating=None):
  trans = MarketTransaction(turker_id = session['turker_id'],
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
  other_args['experiment'] = experiment
  other_args['round'] = cherrypy.session.get('round')
  return env.get_template(page).render(**other_args)

class MarketplacePage:
  _cp_config = {'tools.sessions.on': True}

  @cherrypy.expose
  def index(self):
    return redirect('intro', internal=False)

  @cherrypy.expose
  def intro(self, **amazons_args):
    workerId = amazons_args.get('workerId', 'preview_mode')
    cherrypy.session['turker_id'] = workerId 

    cherrypy.session['submit_domain'] = amazons_args.get('turkSubmitTo', None)
    if cherrypy.session['submit_domain']: # not a preview
      del amazons_args['turkSubmitTo']

    cherrypy.session['amazons_args'] = amazons_args

    # TODO: pick smarter experiment (IE, one you haven't done yet?)
    experiment = Experiment.all().filter('active =', True).get()
    if not experiment:
      return "No valid experiment available, sorry"
    else:
      cherrypy.session['experiment'] = experiment
      return render_for_experiment(
        'intro.html', experiment, in_preview_mode=(workerId=='preview_mode')
      )

  @cherrypy.expose
  def offer(self):
    ses = cherrypy.session
    if not 'round' in cherrypy.session:
      ses['round'] = 0
    ses['round'] += 1 # next round

    experiment = ses['experiment']

    if ses['round'] > experiment.num_rounds_per_subject:
      ses['round'] = 0 # clears session for easier testing 
      # all done, back to mturk now
      url = "%s/mturk/externalSubmit?%s" % (
        ses['submit_domain'], urlencode(ses['amazons_args'])
      )
      return redirect(url, internal=False)
    else:
      #TODO - ask experiment to configure this randomness 
      amount = random.randint(0,10)
      ses['amount'] = amount
      ses['start_time'] = datetime.datetime.now()
      return render_for_experiment('offer.html', experiment, amount=amount)
      
  @cherrypy.expose
  def review(self, accept):
    cherrypy.session['accepted'] = (accept == 'true')
    return render_for_experiment('review.html', cherrypy.session['experiment'])

  @cherrypy.expose
  def finished_round(self, rating=None):
    record_transaction(cherrypy.session, rating) 
    # lets start another round!
    return redirect('offer', internal=False)


  @cherrypy.expose
  def bootstrap(self):
    # sketchy way to start an experiment, TODO find better way
    import bootstrap

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
           
           # setup static files
           'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
            },
      "/js":{'tools.staticdir.dir': 'js',
             'tools.staticdir.on': True},
     }
app = cherrypy.tree.mount(MarketplacePage(), config=cf)
wsgiref.handlers.CGIHandler().run(app)
