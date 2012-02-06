#!/usr/bin/python
"""Set of boto wrappers 
   To set up boto, make sure to add a ~/.boto file with your MTurk details:
   (http://code.google.com/p/boto/wiki/BotoConfig)
"""
print """Usage: 
# (1) generate the experiment: 
# print create_hit(experiment_name)
# (2) pay participants: 
# pay_for_work(hit_list5)

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

TEST_MODE = False
SAFETY_BREAK = False
HTML_FRAME_HEIGHT = 275 #arbitrary and depends on question HTML itself
EXTERNAL_Q_URL = "http://marketplacr.appspot.com/intro"
HIT_DESCRIPTION = "Play a series of simple games with a fellow turker and receive a bonus accordingly"
HIT_TITLE = "Marketplacr experiment"
HIT_KEYWORDS = ["experiment", "easy",]
HIT_BASE_PRICE = 0.05
NUM_TASKS = 10

HIT_CREATE_FAILED = -1

if TEST_MODE:
  print 'in testmode'
  conn = MTurkConnection(host='mechanicalturk.sandbox.amazonaws.com')
else:
  print 'real life'
  conn = MTurkConnection()

def post_html_question(title, description, quals, num_tasks, price, q_url, 
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
    reward=Price(float(price)),
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
  q_url = EXTERNAL_Q_URL
  desc = HIT_DESCRIPTION 
  title = HIT_TITLE 
  base_price = HIT_BASE_PRICE
  quals = Qualifications() # empty

  hit_id = post_html_question(title, desc, quals, 
    num_tasks=NUM_TASKS, price=base_price, q_url=q_url, 
    keywords=HIT_KEYWORDS)
  if hit_id == HIT_CREATE_FAILED:
    raise BaseException("whoa, could not create that hit...")

  import pickle
  try:
    hits = pickle.load(open('hits.pickle', 'rb'))
  except:
    hits = {}
  hits[experiment_name] = hit_id
  pickle.dump(hits, open('hits.pickle', 'wb'))
  return hit_id

def pay_for_work (h_list):
  if SAFETY_BREAK:
    print "Turn off safety break if you're really ready to pay."
    return False
  
  for experiment_name, hit_id in h_list:
    for answer, worker_id, assignment_id in get_answers(hit_id):
      bonus_size = 0.00 #TODO - calculate based on experiment
      if accept_and_pay(worker_id, assignment_id, bonus_size):
        print "paid: %s (+%f)" % (worker_id, bonus_size)
