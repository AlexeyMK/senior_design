To run locally, use (once you have the Google App Engine SDK installed):

> dev_appserver.py . 

Then view at http://localhost:8080/

To push to google app engine, use

> appcfg.py update .

And view at http://marketplacr.appspot.com/

To create a new HIT, use

> python -c "from mturk import create_hit; print create_hit('test')"

And view at:

- Requester: https://requestersandbox.mturk.com/mturk/manageHITs
- Offerer: https://workersandbox.mturk.com/mturk/searchbar?selectedSearchType=hitgroups&searchWords=Marketplacr
