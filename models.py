from google.appengine.ext import db


class Experiment(db.Model):
  experiment_name = db.StringProperty()
  conditions_json = db.StringProperty(default="{}") 
  num_subjects_total = db.IntegerProperty(required=True)
  num_rounds_per_subject = db.IntegerProperty(required=True)
  active = db.BooleanProperty(required=True)
  hit_id = db.StringProperty(required=True)
  base_price_cents = db.IntegerProperty(required=True)

  def __repr__(self):
    return "%s (%s)" % (  
      self.experiment_name, 
      "active" if self.active else "inactive"
    )

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

  def __repr__(self):
    return "<%s: %s was offered %d and %s, rating %s (round %d of %s)>" % (
      self.__class__.__name__,
      self.turker_id, 
      self.amount_offered_cents, 
      "accepted" if self.accepted_offer else "rejected",
      self.rating_left or 'None',
      self.transaction_round,
      self._experiment.id(), # hack to avoid query
    )

#TODO here - 'partner' - bot descriptions, per experiment...
