from models import Experiment
Experiment(hit_id="test", experiment_name="test", num_subjects_total=5, num_rounds_per_subject=5, active=True, base_price_cents=5).put()
