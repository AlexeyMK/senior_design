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
  }
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
