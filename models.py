from google.appengine.ext import db
from google.appengine.api import users


import datetime
import json


class Experiment(db.Model):
  def __init__(self, *args, **kwargs):
    """jsonize the conditions"""
    conditions = kwargs.get('conditions', {})
    kwargs['conditions_json'] = json.dumps(conditions) 
    super(Experiment, self).__init__(*args, **kwargs)

  experiment_name = db.TextProperty()
  conditions_json = db.TextProperty() # TODO
  num_subjects_total = db.IntegerProperty(required=True)
  num_rounds_per_subject = db.IntegerProperty(required=True)
  active = db.BooleanProperty(required=True)
  hit_id = db.TextProperty()#required=True)
  base_price_cents = db.IntegerProperty()#required=True)

class MarketTransaction(db.Model):
  turker_id = db.StringProperty(required=True)
  # partner = something like a config for one of the bots
  # can be inferred from partner later
  amount_offered_cents = db.IntegerProperty(required=True) 
  accepted_offer = db.BooleanProperty(required=True)
  rating_left = db.StringProperty() # left intentionally vague
  experiment = db.ReferenceProperty(Experiment)
  transaction_round = db.IntegerProperty(required=True)
  start_time = db.DateTimeProperty(required=True)
  end_time = db.DateTimeProperty(required=True)

#TODO here - 'partner' - bot descriptions, per experiment...
