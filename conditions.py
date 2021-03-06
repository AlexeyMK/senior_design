import random
from itertools import product
# set of tools for working with a conditions_json object, like smart defaults

CONDITIONS = {
  'thank_on_bad_review': {
    'values': (True, False),
    'default': False,
    'description': "When user votes 1 or 2, tell them we won't pair them with that guy anymore"
  },
  'review_will_be_anonymous': {
    'values': ("anonymous", "public", "dont_mention_it"),
    'default': "dont_mention_it",
    'description': "Ensure user that their review will be shown to the other person (as a proxy for punishment) or that it definitely won't be shown (fear of offending).  Or ignore this part completely"
  },
  'why_leave_a_review': {
    'values': ("personal_gain", "collective_gain", "experimental_validity", "dont_mention_it"),
    'default': "dont_mention_it",
    'description': "When asking the user to leave a review, try different motivational techniques for why they should do it"
  },
  'review_is_mandatory': {
    'values': (True, False),
    'default': False,
    'description': "Force users to leave reviews?",
  },
  'show_earned_so_far': {
    'values': (True, False),
    'default': False,
    'description': "How much money have you made thus far?",
  },
  'choice_set': {
    'values': ('-2..2','1..5', '123', 'updown', 'relative_to_past'), #TODO - half-stars (1-10)
    'default': '1..5',
    'description': "What kind of voting system are we using? (Also, how are we framing it?",
  },
  'wait_for_partner': {
    'values': (True, False),
    'default': False,
    'description': "Do we pretend there's another side making a decision? Take a random time-out and wait every turn before an offer.",
  },
  'comical_response_to_reviews': {
    'values': (True, False),
    'default': False,
    'description': "Do we show funny gifs after positive/negative reviews? A question of adding character to the system."
  },
}

def generate_conditions(input_conditions):
  result = {key:value['default'] for key, value in CONDITIONS.iteritems()}

  # weak imitation of typechecking
  for key, value in input_conditions.iteritems():
    if not key in CONDITIONS:
      raise ValueError("Invalid condition: %s" % key)
    if not value in CONDITIONS[key]['values']:
      raise ValueError("%s is not a valid choice for condition %s" % (
        value, key)) 
    # alright, that worked - overwrite.
    result[key] = value

  return result

def random_set_of_conditions():
  return {key:random.choice(value['values']) 
    for key, value in CONDITIONS.iteritems()}

def all_possible_conditions():
  def options_from_conditions(condition, name):
    return [(name, option) for option in condition['values']]

  named_values = [options_from_conditions(data, name)
    for name, data in CONDITIONS.iteritems()]

  permutations = [dict(conditions) for conditions in product(*named_values)]
  return permutations
