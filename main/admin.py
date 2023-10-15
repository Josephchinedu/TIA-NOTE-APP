from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from main.models import Category, DiaryNote, NoteReminder


# Register your models here.
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class DiaryNoteResource(resources.ModelResource):
    class Meta:
        model = DiaryNote


class NoteReminderResource(resources.ModelResource):
    class Meta:
        model = NoteReminder


class CategoryResourceAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource

    search_fields = [
        "name",
    ]

    list_filter = [
        "created_at",
    ]

    date_hierarchy = "created_at"

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


class DiaryNoteResourceAdmin(ImportExportModelAdmin):
    resource_class = DiaryNoteResource

    search_fields = [
        "owner__first_name",
        "owner__last_name",
        "owner__email",
        "title",
        "category__name",
    ]

    list_filter = ["created_at", "due_date", "priority", "due", "is_finished"]

    raw_id_fields = [
        "owner",
        "category",
    ]

    autocomplete_fields = [
        "owner",
        "category",
    ]

    date_hierarchy = "created_at"

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


class NoteReminderResourceAdmin(ImportExportModelAdmin):
    resource_class = NoteReminderResource

    search_fields = [
        "note__owner__first_name",
        "note__owner__last_name",
        "note__owner__email",
        "note__title",
        "note__category__name",
    ]

    list_filter = [
        "created_at",
        "start_date",
    ]

    raw_id_fields = [
        "note",
    ]

    autocomplete_fields = [
        "note",
    ]

    date_hierarchy = "created_at"

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


admin.site.register(Category, CategoryResourceAdmin)
admin.site.register(DiaryNote, DiaryNoteResourceAdmin)
admin.site.register(NoteReminder, NoteReminderResourceAdmin)
