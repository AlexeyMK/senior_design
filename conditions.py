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
}

def generate_conditions(input_conditions):
  result = {key:value['default'] for key, value in CONDITIONS.iteritems()}

  # weak imitation of typchecking
  for key, value in input_conditions.iteritems():
    if not key in CONDITIONS:
      raise ValueError("Invalid condition: %s" % key)
    if not value in CONDITIONS[key]['values']:
      raise ValueError("%s is not a valid choice for condition %s" % (
        value, key)) 
    # alright, that worked - overwrite.
    result[key] = value

  return result
