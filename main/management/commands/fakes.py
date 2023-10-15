from django.core.management.base import BaseCommand

from main.tasks import celery_save_diary_note_as_pdf, celery_send_diary_note_as_a_file


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        ids = [1, 4]

        celery_send_diary_note_as_a_file.delay(
            item_ids=ids,
            email="joseph4jubilant@gmail.com",
            file_type="pdf",
            name="Joseph",
        )
