To run locally, use (once you have the Google App Engine SDK installed):

> dev_appserver.py . 

Then view at http://localhost:8080/

To push to google app engine, use

> appcfg.py update .

And view at http://marketplacr.appspot.com/

To create a new HIT, follow the instructions at 

> python mturk.py 

And view at:

- Requester: https://requestersandbox.mturk.com/mturk/manageHITs
- Offerer: https://workersandbox.mturk.com/mturk/searchbar?selectedSearchType=hitgroups&searchWords=Marketplacr

(For real hits, view at:)
- Requester: https://requester.mturk.com/mturk/manageHITs
- Offerer: https://mturk.com/mturk/searchbar?selectedSearchType=hitgroups&searchWords=Marketplacr


TODOS:
-----
 - evaluate base case
 - Find bug in current mean squared error (for triples of base_case_2)
 - think about first things we want to vary
