from django_cron import CronJobBase, Schedule
from django.core.management import call_command
import logging


logger = logging.getLogger('event')


class EventCleanup(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = 'event.update_events'

    def do(self):
        print("ran event cleanup")
        logger.info("running cron job")
        try:
            call_command('update_events')
            logger.info("Successfully ran update_events command")
        except Exception as e:
            logger.error(f"Error in cron job: {e}")
        