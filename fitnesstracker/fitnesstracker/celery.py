from __future__ import absolute_import
import os
from celery import Celery, schedules 
from django.conf import settings
from django.core.mail import send_mail
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitnesstracker.settings')
django.setup()
from tracker.views import send_email
# set the default Django settings module for the 'celery' program.
app = Celery('fitnesstracker')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(name="debug_email")
def debug_email():
    print("debug_email")
    return send_email(
        'celery running!',
        'celery running!',
        ['jobie.winser@abingdon.org.uk', 'jobiewinser@live.co.uk', 'jobiewinser@gmail.com']
    )

app.conf.beat_schedule = {
 "run-me-every-ten-seconds": {
 "task": "debug_email",
 "schedule": schedules.crontab(hour="*", minute="*", day_of_week="*")
 }
}





    