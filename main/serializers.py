from rest_framework import serializers

from account.serilaizers import UserSerializer
from main.models import Category, DiaryNote, NoteReminder


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DiaryNoteSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = DiaryNote
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        data = super(DiaryNoteSerializer, self).to_representation(instance)
        user_data = data.pop("owner")
        category_data = data.pop("category")

        data["user"] = user_data
        data["category"] = category_data
        return data


class CreateDiaryNoteSerializer(serializers.Serializer):
    PRIORITY_LEVELS = (
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    )
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    priority_level = serializers.ChoiceField(choices=PRIORITY_LEVELS)
    category = serializers.IntegerField()
    due_date = serializers.DateField()


class DownloadNoteSerializer(serializers.Serializer):
    file_type_options = (("csv", "csv"), ("pdf", "pdf"))
    note_ids = serializers.ListField()
    file_type = serializers.ChoiceField(choices=file_type_options)


class CreateReminderSerializer(serializers.Serializer):
    REMINDER_INTERVALS = (
        ("Thirty_Minutes", "Thirty Minutes"),
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
        ("Yearly", "Yearly"),
    )
    note_id = serializers.IntegerField()
    start_date = serializers.DateField()
    reminder_interval = serializers.ChoiceField(choices=REMINDER_INTERVALS)
    reminder_message = serializers.CharField(max_length=255)


class UpdateReminderSerializer(serializers.Serializer):
    REMINDER_INTERVALS = (
        ("Thirty_Minutes", "Thirty Minutes"),
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
        ("Yearly", "Yearly"),
    )
    start_date = serializers.DateField()
    reminder_interval = serializers.ChoiceField(choices=REMINDER_INTERVALS)
    reminder_message = serializers.CharField(max_length=255)


class NoteReminderSerializer(serializers.ModelSerializer):
    note = DiaryNoteSerializer()

    class Meta:
        model = NoteReminder
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        data = super(NoteReminderSerializer, self).to_representation(instance)
        note_data = data.pop("note")

        data["note"] = note_data
        return data
