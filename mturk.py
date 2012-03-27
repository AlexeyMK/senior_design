"""Set of boto wrappers 
   To set up boto, make sure to add a ~/.boto file with your MTurk details:
   (http://code.google.com/p/boto/wiki/BotoConfig)
"""

#TODO: be more specific with imports
from boto.mturk.connection import *
from boto.mturk.question import *
from boto.mturk.price import *
from boto.mturk.qualification import *
from boto.s3 import *
from os.path import *

import urllib
import time
import logging
import pickle
import csv
import json
from conditions import all_possible_conditions, generate_conditions

logger = logging.getLogger()
logger.setLevel(logging.INFO)
TEST_MODE = True
LOCAL_MODE = False
SAFETY_BREAK = True
HTML_FRAME_HEIGHT = 275 #arbitrary and depends on question HTML itself
EXTERNAL_Q_URL = "http://localhost:8080/intro" if LOCAL_MODE else \
                 "http://marketplacr.appspot.com/intro"
HIT_DESCRIPTION = "Play a series of simple games with a fellow turker and receive a bonus accordingly"
HIT_TITLE = "Marketplacr experiment"
HIT_KEYWORDS = ["experiment", "easy",]
BASE_PRICE_CENTS = 3
NUM_ROUNDS_PER_SUBJECT = 5

HIT_CREATE_FAILED = -1

if TEST_MODE:
  print 'in testmode'
  conn = MTurkConnection(host='mechanicalturk.sandbox.amazonaws.com')
else:
  print 'real life'
  conn = MTurkConnection()

def post_html_question(title, description, quals, num_tasks, price_cents, q_url, 
  duration_s=300, keywords=None):
  """Wrapper for creating & posting 'ExternalQuestion' on MTurk.
     
     see git.to/externalq for Amazon's ExternalQuestion docs
     see git.to/createhit for boto's create_hit method

     quals -- Qualifications object list. Use build_quals to create.
     price -- float (IE, 0.05 for 5 cents)
     duration_s -- max number of seconds the HIT can take. 

     Return the resulting HITId or -1 on failure.   
  """  
  if keywords == None: 
    keywords = []

  question = ExternalQuestion(q_url, HTML_FRAME_HEIGHT)
  
  result = conn.create_hit(
    question=question,
    title=title,
    description=description,
    keywords=keywords,
    reward=Price(price_cents/100.0),
    max_assignments=num_tasks,
    duration=duration_s,
    qualifications=quals
  )
  return result[0].HITId or HIT_CREATE_FAILED#resulting hit ID or broken

def get_answers(hit_id):
  """return a list of tuples (answer, worker_id, assignment_id)"""
  # TODO: Support >100, tasks/HIT. Here's how: first call getHit, get 
  # assignments, call get_assignments on every hundred and join them.

  assignments = conn.get_assignments(hit_id=hit_id, page_size=100)
  return [(assign.answers[0],
      	   assign.WorkerId,
           assign.AssignmentId) for assign in assignments]

def accept_and_pay(worker_id, assign_id, bonus_price=0.00, 
	   reason="Congratulations!"):
  """pays for assignment; returns False if something went wrong, else True"""
  try:
    result = conn.approve_assignment(assign_id)
    #TODO: make sure to avoid the possibility of paying the same bonus twice 
    if bonus_price > 0:
      conn.grant_bonus(worker_id, assign_id, Price(amount=bonus_price), reason)
  except MTurkRequestError:
    #TODO: less embarrasing error handling
    print "looks like this one was already paid for. or, any other error" 
    return False# no bonus if already paid for
  return True

def reject(assign_id, reason="That was not correct"):
  try:
    conn.reject_assignment(assign_id, reason)
    return True
  except BaseException:
    #TODO: Less disgustingly general exception here
    print "looks like this one was already rejected. or, any other error" 
    return False

def create_hit(experiment_name, num_tasks): 
  quals = Qualifications() # empty
  url = "%s?%s" % (EXTERNAL_Q_URL, urllib.urlencode({
    "experiment_name":experiment_name
  }))

  hit_id = post_html_question(HIT_TITLE, HIT_DESCRIPTION, quals, 
    num_tasks=num_tasks, price_cents=BASE_PRICE_CENTS, q_url=url,
    keywords=HIT_KEYWORDS)
  if hit_id == HIT_CREATE_FAILED:
    raise BaseException("whoa, could not create that hit...")

  try:
    hits = pickle.load(open('hits.pickle', 'rb'))
  except:
    hits = {}
  hits[experiment_name] = hit_id
  pickle.dump(hits, open('hits.pickle', 'wb'))
  return hit_id

def pay_for_work(h_list):
  total_paid = 0.0
  for experiment_name, hit_id in h_list:
    answers = get_answers(hit_id)
    worker_set = set([(worker, asgn_id) for ans, worker, asgn_id in answers])
    for worker_id, assignment_id in worker_set:
      bonus_size = calculate_bonus_size(
        experiment_name, worker_id, assignment_id)/100.0
      total_paid += bonus_size
      if SAFETY_BREAK:
        print "Turn off safety break if you're really ready to pay."
        print 'would have paid %s amount %f for assignment %s' % \
          (worker_id, bonus_size, assignment_id) 
      else:
        accept_and_pay(worker_id, assignment_id, bonus_size)
        print "paid: %s (+%f)" % (worker_id, bonus_size)

  print "Paid (or would have paid) total of %02f" % total_paid


#############################################################
# Marketplacr specific code
#############################################################
from google.appengine.ext import db
import models

if not LOCAL_MODE:
  import remote_api
  # Let's make sure to hit the remote version of marketplacr here
  # http://code.google.com/appengine/articles/remote_api.html
  remote_api.attach()

def create_experiment(name, num_tasks=10, **experiment_kwargs):
  """ recommended arguments for experiment: 
  
  """
  conditions = generate_conditions(experiment_kwargs)
  hit_id = "local_mode" if LOCAL_MODE else create_hit(name, num_tasks)
  if not hit_id:
    raise BaseException("failed to create HIT, so not making experiment")

  experiment = models.Experiment(
    base_price_cents=BASE_PRICE_CENTS,
    num_rounds_per_subject=NUM_ROUNDS_PER_SUBJECT,
    num_subjects_total=num_tasks,
    experiment_name=name,
    hit_id=hit_id,
    conditions_json=json.dumps(conditions),
    active=True,
  )

  print "Experiment %s created." % experiment.experiment_name
  experiment.put()
  if TEST_MODE:
    print "Test at %s?experiment_name=%s&assignmentId=BS1&hitId=BS2&workerId=BS3%d&&turkSubmitTo=https://workersandbox.mturk.com" % (
      EXTERNAL_Q_URL, experiment.experiment_name, int(time.time()))

  return experiment

def pay_for_experiment(experiment_name):
  query = db.GqlQuery("SELECT * FROM Experiment WHERE experiment_name = :1",
                       experiment_name)

  if query.count() == 0:
    raise Exception("Could not find experiment %s" % experiment_name)
  elif query.count() > 1:
    raise Exception("Found too many experiments named %s" % experiment_name)

  experiment = query.get()
  #TODO - make this generic (IE, mturk layer takes a func to calculate pay)
  pay_for_work([(experiment_name, experiment.hit_id), ])

  # if you're paying, this experiment is done
  if not SAFETY_BREAK:
    experiment.active = False
    experiment.put()

def calculate_bonus_size(experiment_name, worker_id, assignment_hit_id):
  #TODO use hit as well here
  experiment = models.Experiment.all().filter(
    "experiment_name =", experiment_name).get() 
  query = db.GqlQuery("""SELECT * FROM MarketTransaction WHERE 
      turker_id = :1 AND experiment = :2""", 
    worker_id, experiment.key())
                      
  bonus_cents = 0
  for idx, transaction in enumerate(query):
    if transaction.accepted_offer:
      logger.info("%s accepted %d" % (worker_id, transaction.amount_offered_cents))
      if idx < 5:
        bonus_cents += transaction.amount_offered_cents
      else:
        logger.info("%s got too greedy, tried more than 5 rounds!" % 
          worker_id)
        break
    else: 
      logger.info("%s rejected %d" % (worker_id, transaction.amount_offered_cents))

  return bonus_cents 

def analyze_experiment(experiment_name):
  experiment = db.GqlQuery("SELECT * FROM Experiment WHERE experiment_name = :1", 
    experiment_name).get()
  if not experiment:
    raise Exception("Could not find experiment named %s" % experiment_name)
  transactions = gather_experiment_data(experiment)
  # for now - exclude transations where no rating was left
  transactions = [t for t in transactions if t.rating_left is not None]
  write_results_to_csv(transactions, "results/%s.csv" % experiment_name)
  write_conditions_to_json(experiment, "results/%s.json" % experiment_name)
  import analysis 
  analysis_trips = [
    (t.amount_offered_cents, int(t.rating_left), t.accepted_offer) 
  for t in transactions]

  error = analysis.mean_squared_error(analysis_trips)
  print '-'*80 
  print "Number of transactions: %d" % len(transactions)
  print "Number of subjects: %d" % len(set(t.turker_id for t in transactions))
  print "Root Mean Squared Error of %s: %f" % (experiment_name, error)
  print '-'*80 
  analysis.plot_linreg(analysis_trips, 
                       save_fname="results/%s.png" % experiment_name)
  
def gather_experiment_data(experiment): 
  """produces a list of MarketTransaction objects"""
  experiment_transactions = db.GqlQuery(
    "SELECT * FROM MarketTransaction WHERE experiment = :1", experiment.key()) 

  return experiment_transactions 

def write_conditions_to_json(experiment, output_name):
  # for legacy's sake, re-generate conditions 
  conditions = generate_conditions(json.loads(experiment.conditions_json))
  with open(output_name, 'w') as writer:
    writer.write(json.dumps(conditions))

def write_results_to_csv(transactions, output_name):
  """ takes list of Transaction objects and writes them to csv"""
  writer = csv.writer(open(output_name, 'w'))
  writer.writerow([
    "Amount offered", "Rating Left", "Accepted offer?", "Turker ID"])
  writer.writerows([
    (t.amount_offered_cents, t.rating_left, t.accepted_offer, t.turker_id) 
  for t in transactions])

def run_every_possible_experiment(prefix, num_tasks_each):
  for idx, conditions in enumerate(all_possible_conditions()):
    create_experiment("%s_%d" % (prefix, idx+1), num_tasks_each, **conditions)


if __name__ == "__main__":
  print """Usage: 
  # (1) generate the experiment: 
  # print create_experiment(experiment_name, num_tasks=5, cond1=val, cond2=val, etc)
  # (2) pay participants: 
  # pay_for_experiment(experiment_name)
  # (3) download and save results:
  # analyze_experiment(experiment_name) 

  In testmode, you can verify that your thing got pushed here:
  Requester: https://requestersandbox.mturk.com/mturk/manageHITs
  Turker: https://workersandbox.mturk.com/mturk/ and search for your task 

  Available experiments:
  """
  experiments = [t for t in db.GqlQuery("Select * FROM Experiment")]
  for idx, experiment in enumerate(experiments):
    print "(%d) %s" % (idx + 1, experiment)

  print "(available in the variable 'experiments' if you need them directly)" 
