
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from .task_one import task_1
from .task_two import task_2
from api.match.scheduled_task import check_due_matches


job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone=utc)


def start():
    # scheduler.add_job(task_1, 'interval', seconds=31)
    # scheduler.add_job(task_2, 'interval', seconds=31)
    # scheduler.add_job(check_due_matches, 'interval', seconds=31)
    scheduler.start()
