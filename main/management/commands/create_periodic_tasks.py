import pytz
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask


def periodic_task_every_30_minutes():
    
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=30,
        period=IntervalSchedule.MINUTES,
    )

    # check if the task already exists
    # if not, create it
    start_datetime = timezone.now() + timezone.timedelta(seconds=10)

    if not PeriodicTask.objects.filter(
        name="30 minutes reminder",
        task="main.tasks.celery_thirty_minutes_reminder",
        enabled=True,
    ).exists():
        PeriodicTask.objects.create(
            interval=schedule,
            name="30 minutes reminder",
            task="main.tasks.celery_thirty_minutes_reminder",
            start_time=start_datetime,
        )


def periodic_task_daily():
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="0",
        hour="0",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
    )

    # check if the task already exists
    # if not, create it
    start_datetime = timezone.now() + timezone.timedelta(seconds=10)

    if not PeriodicTask.objects.filter(
        name="daily reminder",
        task="main.tasks.celery_daily_reminder",
        enabled=True,
    ).exists():
        PeriodicTask.objects.create(
            crontab=schedule,
            name="daily reminder",
            task="main.tasks.celery_daily_reminder",
            start_time=start_datetime,
        )


def periodic_task_weekly():
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="0",
        hour="0",
        day_of_week="0",
        day_of_month="*",
        month_of_year="*",
    )

    # check if the task already exists
    # if not, create it
    start_datetime = timezone.now() + timezone.timedelta(seconds=10)

    if not PeriodicTask.objects.filter(
        name="weekly reminder",
        task="main.tasks.celery_weekly_reminder",
        enabled=True,
    ).exists():
        PeriodicTask.objects.create(
            crontab=schedule,
            name="weekly reminder",
            task="main.tasks.celery_weekly_reminder",
            start_time=start_datetime,
        )


def periodic_task_monthly():
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="0",
        hour="0",
        day_of_week="0",
        day_of_month="1",
        month_of_year="*",
    )

    # check if the task already exists
    # if not, create it
    start_datetime = timezone.now() + timezone.timedelta(seconds=10)

    if not PeriodicTask.objects.filter(
        name="monthly reminder",
        task="main.tasks.celery_monthly_reminder",
        enabled=True,
    ).exists():
        PeriodicTask.objects.create(
            crontab=schedule,
            name="monthly reminder",
            task="main.tasks.celery_monthly_reminder",
            start_time=start_datetime,
        )


def periodic_task_yearly():
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="0",
        hour="0",
        day_of_week="0",
        day_of_month="1",
        month_of_year="1",
    )

    # check if the task already exists
    # if not, create it
    start_datetime = timezone.now() + timezone.timedelta(seconds=10)

    if not PeriodicTask.objects.filter(
        name="yearly reminder",
        task="main.tasks.celery_yearly_reminder",
        enabled=True,
    ).exists():
        PeriodicTask.objects.create(
            crontab=schedule,
            name="yearly reminder",
            task="main.tasks.celery_yearly_reminder",
            start_time=start_datetime,
        )


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        periodic_task_every_30_minutes()

        periodic_task_daily()

        periodic_task_weekly()

        periodic_task_monthly()

        periodic_task_yearly()
