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

List of experiments to run (+ estimates)
===========================

Available Conditions:
---------------------
(see conditions.py)

Next:
----
- [10m] Text: Motivate leaving a review, personal gain (filtering out bad partners)
- [10m] Text: Motivate leaving a review, collective gain (cleans system, important)
- [10m] Text: Motivate leaving a review, base case (experimental validity...)
- [30m] Force leaving a review to be mandatory 

Test whether the above work

- [1hr] Show amount of $$ earned so far

- test these

- change turkers to something like 25 

- start adding more experiments

Later:
------

- [2hr] Show (vs don't show) past ratings
    - [10m] Show past rating in diffent scale (say out of 10, or ranking) 
    - [1hr] Emphasize polarized past reviews
- [4hr] Add more personality to the other side (name profile, etc)
- [1hr] Rank past interactions instead of asking individually (rank "this vs last")
- [5hr] Rank past interactions instead of asking individually (rank "interactions this session")
- [4hr] Pay for accurate reviews (immediately when left)
  - [2hr] Pay for accurate reviews (at the end, and let them know before)
- [3hr[ Animation when review is left (happy face/sad face, trash can, etc)
- [30m] Fewer choices: Thumbs up/down
  - [5m] Fewer choices: 1/2/3 
  - [5m] More choices: 1-->10
  - [5m] Different framing (-2...2)
- [2hr] Rate on speed AND fairness rather than 'in general'
- [5hr] Ask for all feedback afterwards (end of session)
- [2hr] Ask for all feedback afterwards (contact via mturk)

TODOS:
-----
 - turkers appear to be abusing the system, make them stop (restrictions)
 - ensure we have code for "ineligible for experiment"
 - actually send email when done (super-simple with mailgun)
 - list of active experiments (1,2,3) and maybe shovel integration 

 - some sort of tool to validate that conditions are being used correctly (relies on hard-coded dict of known conditions)
 - do a slightly nicer statistical job of analyzing the results 
 - base jinja2 template which puts conditions into a top-level JSON blockj:w
 - more experiments
