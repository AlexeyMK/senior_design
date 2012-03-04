"""Set of boto wrappers 
   To set up boto, make sure to add a ~/.boto file with your MTurk details:
   (http://code.google.com/p/boto/wiki/BotoConfig)
"""
print """Usage: 
# (1) generate the experiment: 
# print create_experiment(experiment_name)
# (2) pay participants: 
# pay_for_experiment(experiment_name)
# (3) download and save results:
# data_triples = gather_experiment_data(experiment_name)
# write_results_to_csv(data_triples, "results.csv")
# (4) analyze resuls 
# import analysis 
# error = mean_squared_error(data_triples)
# plot_linreg(data_triples) 

In testmode, you can verify that your thing got pushed here:
Requester: https://requestersandbox.mturk.com/mturk/manageHITs
Turker: https://workersandbox.mturk.com/mturk/ and search for your task 
"""

#TODO: be more specific with imports
from boto.mturk.connection import *
from boto.mturk.question import *
from boto.mturk.price import *
from boto.mturk.qualification import *
from boto.s3 import *
from os.path import *
import urllib
import sys,os
import logging
import pickle
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)
TEST_MODE = False 
SAFETY_BREAK = True 
HTML_FRAME_HEIGHT = 275 #arbitrary and depends on question HTML itself
EXTERNAL_Q_URL = "http://marketplacr.appspot.com/intro"
HIT_DESCRIPTION = "Play a series of simple games with a fellow turker and receive a bonus accordingly"
HIT_TITLE = "Marketplacr experiment"
HIT_KEYWORDS = ["experiment", "easy",]
BASE_PRICE_CENTS = 3
NUM_TASKS = 10
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

def create_hit(experiment_name): 
  # TODO - parametrize by experiment conditions
  quals = Qualifications() # empty

  hit_id = post_html_question(HIT_TITLE, HIT_DESCRIPTION, quals, 
    num_tasks=NUM_TASKS, price_cents=BASE_PRICE_CENTS, q_url=EXTERNAL_Q_URL,
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
  bonuses_already_paid = set()
  for experiment_name, hit_id in h_list:
    for answer, worker_id, assignment_id in get_answers(hit_id):
      if not worker_id in bonuses_already_paid:
        bonus_size = calculate_bonus_size(worker_id, assignment_id)/100.0
        bonuses_already_paid.add(worker_id)
      else:
        bonus_size = 0 
      if SAFETY_BREAK:
        print "Turn off safety break if you're really ready to pay."
        print 'would have paid %s amount %f for assignment %s' % \
          (worker_id, bonus_size, assignment_id) 
      else:
        accept_and_pay(worker_id, assignment_id, bonus_size)
        print "paid: %s (+%f)" % (worker_id, bonus_size)


#############################################################
# Marketplacr specific code
#############################################################
from google.appengine.ext import db
import models
import remote_api
# Let's make sure to hit the remote version of marketplacr here
# http://code.google.com/appengine/articles/remote_api.html
remote_api.attach()

def create_experiment(name, **experiment_kwargs):
  """ recommended arguments for experiment: 
  
  """
  hit_id = create_hit(name)
  if not hit_id:
    raise BaseException("failed to create HIT, so not making experiment")

  experiment = models.Experiment(
    base_price_cents=BASE_PRICE_CENTS,
    num_rounds_per_subject=NUM_ROUNDS_PER_SUBJECT,
    num_subjects_total=NUM_TASKS,
    experiment_name=name,
    hit_id=hit_id,
    conditions=experiment_kwargs.get('conditions', {}),
    active=True,
  )

  print "Experiment %s created." % experiment.experiment_name
  experiment.put()
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

def calculate_bonus_size(worker_id, assignment_hit_id):
  #TODO use hit as well here
  query = db.GqlQuery("SELECT * FROM MarketTransaction WHERE turker_id = :1",
                      worker_id)
  bonus_cents = 0
  for transaction in query:
    if transaction.accepted_offer:
      logger.info("%s accepted %d" % (worker_id, transaction.amount_offered_cents))
      bonus_cents += transaction.amount_offered_cents
    else: 
      logger.info("%s rejected %d" % (worker_id, transaction.amount_offered_cents))

  return bonus_cents 
  
def gather_experiment_data(experiment_name): 
  """produces a list of (amt, rating, accept/reject)""" 
  experiment = db.GqlQuery("SELECT * FROM Experiment WHERE experiment_name = :1", 
    experiment_name).get()
  if not experiment:
    raise Exception("Could not find experiment named %s" % experiment_name)
  experiment_transactions = db.GqlQuery(
    "SELECT * FROM MarketTransaction WHERE experiment = :1", experiment.key()) 
  #TODO - just use experiment.transaction_set or similar here
  offers = [(t.amount_offered_cents, t.rating_left, t.accepted_offer)
    for t in experiment_transactions]

  return offers

def write_results_to_csv(csv_triples, output_name):
  """ takes gather_experiment_data triples and writes them to csv"""
  writer = csv.writer(open(output_name, 'w'))
  writer.writerow(["Amount offered", "Rating Left", "Accepted offer?"])
  writer.writerows(csv_triples)
