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
- [30m] wait for other delay
- [1hr] Pay for accurate reviews (immediately when left) define 'accurate' - by buckets, 1c bonuses. Let them know immediately.

Later:
------
- [30m] More choices: 1-->10 TODO: ask jessica
- [2hr] Animation when review is left (happy face/sad face, trash can, etc)
- [2hr] Ask for all feedback afterwards (end of session) (include quality reminder)
- [2hr] Show (vs don't show) past ratings
    - show 'correct' ratings instead
    - show 'true' ratings from all past experiments (calculate first)

Probably Wont Happen:
---------------------
- [2hr] Rate on speed AND fairness rather than 'in general'
- [2hr] Pay for accurate reviews (at the end, and let them know before)
- [1hr] (show past reviews) Emphasize polarized past reviews
- [5hr] Rank past interactions instead of asking individually (rank "interactions this session")
- [4hr] Add more personality to the other side (name profile, etc)
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
