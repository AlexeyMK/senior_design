import cherrypy
import json
import wsgiref.handlers
import random
import sys, os
import datetime
import logging

from cherrypy.lib.cptools import redirect
from jinja2 import Environment, FileSystemLoader
from google.appengine.api import memcache
from google import appengine
from urllib import urlencode

from conditions import generate_conditions
from models import *

# patch sys memcache module locations to use GAE memcache
sys.modules['memcache'] = memcache
env = Environment(loader=FileSystemLoader('templates'))

def record_transaction(session, rating=None, amount=None):
  trans = MarketTransaction(turker_id = session['turker_id'],
                   amount_offered_cents = amount or session['amount'],
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
  other_args['conditions'] = generate_conditions(
    json.loads(experiment.conditions_json))
  other_args['experiment'] = experiment
  other_args['earned_so_far_cents'] = cherrypy.session['earned_so_far_cents']
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

    if workerId != 'preview_mode':
      past_transaction = MarketTransaction.all().filter(
        'turker_id = ', workerId).get()
      if past_transaction:
        return "You have already participated in one of our experiments"

    cherrypy.session['turker_id'] = workerId 

    cherrypy.session['submit_domain'] = amazons_args.get('turkSubmitTo', None)
    if cherrypy.session['submit_domain']: # not a preview
      del amazons_args['turkSubmitTo']

    cherrypy.session['amazons_args'] = amazons_args
    cherrypy.session['earned_so_far_cents'] = 0

    experiment_name = amazons_args.get('experiment_name', None)
    if not experiment_name:
      return "Can't find experiment_name in arguments"
    experiment = Experiment.all().filter(
      'experiment_name =', experiment_name).get()
    if not experiment:
      return "Can't find experiment %s, sorry" % experiment_name
    elif not experiment.active:
      return "That experiment is no longer active, sorry"
    else:
      cherrypy.session['experiment'] = experiment
      return render_for_experiment(
        'intro.html', experiment, in_preview_mode=(workerId=='preview_mode')
      )

  @cherrypy.expose
  def offer(self):
    ses = cherrypy.session
    if not 'round' in cherrypy.session:
      ses['round'] = 1

    experiment = ses['experiment']

    if ses['round'] > experiment.num_rounds_per_subject:
      # all done, back to mturk now
      return redirect('finished_experiment', internal=False)
    else:
      #TODO - ask experiment to configure this randomness 
      amount = random.randint(0,10)
      ses['last_amount'] = ses.get('amount')
      ses['amount'] = amount
      ses['start_time'] = datetime.datetime.now()
      return render_for_experiment('offer.html', experiment, amount=amount)
      
  @cherrypy.expose
  def review(self, accept):
    ses = cherrypy.session
    ses['accepted'] = (accept == 'true')
    if ses['accepted']:
      ses['earned_so_far_cents']+= ses['amount']

    # if no need for review, just keep going
    if condition_get('choice_set') == 'relative_to_past' and ses['round'] == 1:
      return self.finished_round()
      # can't compare relative to past on round 1 (no past)
      # BUG; having a redirect here restarts the things we added to the session.
      # very weird.
      ## return redirect('finished_round', internal=True)
    else:
      return render_for_experiment('review.html', ses['experiment'])

  @cherrypy.expose
  def finished_round(self, rating=None):
    ses = cherrypy.session
    if condition_get('choice_set') == 'relative_to_past': 
      if ses['round'] > 1:
        # save relative ratings
        if rating == 'prefer_current':
          record_transaction(ses, "5", amount=ses['amount']) 
          record_transaction(ses, "1", amount=ses['last_amount']) 
        elif rating == 'prefer_last':
          record_transaction(ses, "1", amount=ses['amount']) 
          record_transaction(ses, "5", amount=ses['last_amount']) 
    else:
      record_transaction(ses, rating) 

    ses['round'] += 1

    if ses['round'] > ses['experiment'].num_rounds_per_subject:
      # all done, back to mturk now
      return redirect('finished_experiment', internal=False)
    else:
    # lets start another round!
      return redirect('offer', internal=False)

  @cherrypy.expose
  def finished_experiment(self, rating=None):
    ses = cherrypy.session
    if ses['round'] < ses['experiment'].num_rounds_per_subject:
      return "You're not done yet, what are you doing here?"

    url = "%s/mturk/externalSubmit?%s" % (
      ses['submit_domain'], urlencode(ses['amazons_args'])
    )
    logging.info("telling user %s to go to %s" % (ses['turker_id'], url))
    return """All done! Click <a href="%s">here</a> to submit.""" % url

  @cherrypy.expose
  def bootstrap(self):
    # sketchy way to start an experiment, TODO find better way
    # this has gross side-effects and is unprotected
    import bootstrap

def condition_get(condition_name):
  conditions = generate_conditions(
    json.loads(cherrypy.session['experiment'].conditions_json))
  return conditions.get(condition_name)

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
