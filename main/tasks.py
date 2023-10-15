import time
from datetime import datetime

import pandas as pd
import pytz
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from main.helpers.emails_helper import EmailHandler
from main.models import DiaryNote, NoteReminder


@shared_task
def celery_send_diary_note_as_a_file(
    item_ids: list, email: str, file_type: str, name: str
):
    """
    THIS IS A CELERY TASK

    Args:
        item_ids (list): list of item ids
        email (str): email of the user
        file_type (str): file type

    Description:
        This function saves the diary note as a file and sends it to the user's email
        - file format are "csv" and "pdf"
    """

    if file_type == "csv":
        file_name = f"{email}{time.time()}_diary_note.csv"
        celery_save_diary_note_as_csv(
            item_ids=item_ids, file_name=file_name, email=email
        )

        EmailHandler(email=email).send_file_report_ro_user(
            file_name=file_name, first_name=name, year=datetime.now().year
        )

        return {"file_name": file_name}

    elif file_type == "pdf":
        file_name = f"{email}{time.time()}_diary_note.pdf"
        celery_save_diary_note_as_pdf(
            item_ids=item_ids, email=email, name=name, file_name=file_name
        )

        EmailHandler(email=email).send_file_report_ro_user(
            file_name=file_name, first_name=name, year=datetime.now().year
        )

        return {"file_name": file_name}
    else:
        raise ValueError("File type not supported")


@shared_task
def celery_save_diary_note_as_pdf(
    item_ids: list, email: str, name: str, file_name: str
):
    """
    THIS IS A CELERY TASK

    Args:
        item_ids (list): list of item ids
        email (str): email of the user
        name (str): name of the user
        file_name (str): name of the file

    Description:
        This function saves the diary note queryset as a pdf file
    """
    notes = DiaryNote.objects.filter(
        id__in=item_ids, owner__email=email
    ).select_related("owner", "category")

    html_content = render_to_string(
        "diary_pdf.html",
        {
            "email": email,
            "notes": notes,
            "name": name,
            "current_year": datetime.now().year,
        },
    )

    result_file = open(file_name, "wb")
    pisa_status = pisa.CreatePDF(html_content, dest=result_file)
    result_file.close()

    if pisa_status.err:
        print("Error while creating PDF")
    else:
        print("PDF created")


@shared_task
def celery_save_diary_note_as_csv(item_ids: list, file_name: str, email: str):
    """
    THIS IS A CELERY TASK

    Args:
        item_ids (list): list of item ids
        email (str): email of the user

    Description:
        This function saves the diary note as a csv file and sends it to the user's email
    """
    notes = list(
        DiaryNote.objects.filter(id__in=item_ids, owner__email=email)
        .select_related("owner", "category")
        .values(
            "owner__first_name",
            "owner__last_name",
            "title",
            "content",
            "category__name",
            "priority",
            "due",
            "is_finished",
            "due_date",
        )
    )

    df = pd.DataFrame.from_records(notes)

    df.to_csv(file_name)


@shared_task
def celery_thirty_minutes_reminder():
    """
    THIS IS A CELERY TASK

    Description:
        This function sends a reminder to the user every 30 minutes for thier notes
    """

    TODAY = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    TODAYS_DATE = TODAY.date()

    qs = NoteReminder.objects.filter(
        reminder_interval="Thirty_Minutes", start_date__gte=TODAYS_DATE
    ).select_related("note", "note__owner", "note__category")

    if qs.exists():
        for item in qs:
            EmailHandler(email=item.note.owner.email).send_reminder(
                reminder_message=item.reminder_message,
                first_name=item.note.owner.first_name,
                note_title=item.note.title,
                year=TODAYS_DATE.year,
            )


@shared_task
def celery_daily_reminder():
    """
    THIS IS A CELERY TASK

    Description:
        This function sends a reminder to the user every day for thier notes
    """

    TODAY = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    TODAYS_DATE = TODAY.date()

    qs = NoteReminder.objects.filter(
        reminder_interval="Daily", start_date__gte=TODAYS_DATE
    ).select_related("note", "note__owner", "note__category")

    if qs.exists():
        for item in qs:
            EmailHandler(email=item.note.owner.email).send_reminder(
                reminder_message=item.reminder_message,
                first_name=item.note.owner.first_name,
                note_title=item.note.title,
                year=TODAYS_DATE.year,
            )


@shared_task
def celery_weekly_reminder():
    """
    THIS IS A CELERY TASK

    Description:
        This function sends a reminder to the user every week for thier notes
    """

    TODAY = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    TODAYS_DATE = TODAY.date()

    qs = NoteReminder.objects.filter(
        reminder_interval="Weekly", start_date__gte=TODAYS_DATE
    ).select_related("note", "note__owner", "note__category")

    if qs.exists():
        for item in qs:
            EmailHandler(email=item.note.owner.email).send_reminder(
                reminder_message=item.reminder_message,
                first_name=item.note.owner.first_name,
                note_title=item.note.title,
                year=TODAYS_DATE.year,
            )


@shared_task
def celery_monthly_reminder():
    """
    THIS IS A CELERY TASK

    Description:
        This function sends a reminder to the user every month for thier notes
    """

    TODAY = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    TODAYS_DATE = TODAY.date()

    qs = NoteReminder.objects.filter(
        reminder_interval="Monthly", start_date__gte=TODAYS_DATE
    ).select_related("note", "note__owner", "note__category")

    if qs.exists():
        for item in qs:
            EmailHandler(email=item.note.owner.email).send_reminder(
                reminder_message=item.reminder_message,
                first_name=item.note.owner.first_name,
                note_title=item.note.title,
                year=TODAYS_DATE.year,
            )


@shared_task
def celery_yearly_reminder():
    """
    THIS IS A CELERY TASK

    Description:
        This function sends a reminder to the user every year for thier notes
    """

    TODAY = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    TODAYS_DATE = TODAY.date()

    qs = NoteReminder.objects.filter(
        reminder_interval="Yearly", start_date__gte=TODAYS_DATE
    ).select_related("note", "note__owner", "note__category")

    if qs.exists():
        for item in qs:
            EmailHandler(email=item.note.owner.email).send_reminder(
                reminder_message=item.reminder_message,
                first_name=item.note.owner.first_name,
                note_title=item.note.title,
                year=TODAYS_DATE.year,
            )
