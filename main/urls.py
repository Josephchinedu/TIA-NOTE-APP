from django.urls import path

from main.views import (
    DiaryNoteApiView,
    DownloadNoteToFile,
    NoteCategoryApiView,
    NoteReminderApiView,
)

urlpatterns = [
    path("categories/", NoteCategoryApiView.as_view(), name="category-list"),
    path("note/", DiaryNoteApiView.as_view(), name="note-list"),
    path("download_note/", DownloadNoteToFile.as_view(), name="download-note"),
    path("reminder/", NoteReminderApiView.as_view(), name="reminder-list"),
]
