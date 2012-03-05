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
 - make the recommended instructions work (maybe one step?) - need to int the triples
 - make list of all test ideas
 - figure out which tests are easiest to run next (2 or 3)
 - evaluate base case
 - think about first things we want to vary
