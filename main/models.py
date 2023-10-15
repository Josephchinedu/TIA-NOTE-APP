from django.db import models

from account.managers import BaseModel
from account.models import User

# Create your models here.


class Category(BaseModel):
    OPTIONS = (
        ("Personal_Growth", "Personal Growth"),
        ("Work", "Work"),
        ("Health", "Health"),
        ("Travel", "Travel"),
        ("Family", "Family"),
        ("Hobbies", "Hobbies"),
        ("Goals", "Goals"),
        ("Mental_Health", "Mental Health"),
        ("Daily_Reflections", "Daily Reflections"),
        ("Inspiration", "Inspiration"),
        ("Education", "Education"),
        ("Finance", "Finance"),
        ("Recipes", "Recipes"),
        ("Books", "Books"),
        ("Movies", "Movies"),
        ("Music", "Music"),
        ("Art", "Art"),
        ("Technology", "Technology"),
        ("Fitness", "Fitness"),
        ("Outdoors", "Outdoors"),
        ("Creativity", "Creativity"),
        ("Mindfulness", "Mindfulness"),
        ("Self_Care", "Self Care"),
        ("History", "History"),
        ("Sports", "Sports"),
        ("Food", "Food"),
        ("Fashion", "Fashion"),
        ("Relationships", "Relationships"),
        ("Pets", "Pets"),
        ("Nature", "Nature"),
    )

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CATEGORY"
        verbose_name_plural = "CATEGORIES"


class DiaryNote(BaseModel):
    PRIORITY_LEVELS = (
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_note")
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.CharField(max_length=6, choices=PRIORITY_LEVELS, default="Low")
    due_date = models.DateField()
    due = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = "DIARY NOTE"
        verbose_name_plural = "DIARY NOTES"

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls, user):
        """
        Get all diary notes of a user

        Args:
            user (User): User object

        Returns:
            QuerySet: QuerySet of DiaryNote objects

        """
        return cls.objects.filter(owner=user).select_related("owner", "category")

    @classmethod
    def get_note_by_id(cls, user, id):
        """
        Get a diary note by id

        Args:
            user (User): User object
            id (int): id of the diary note

        Returns:
            DiaryNote: DiaryNote object

        """
        try:
            instance = cls.objects.get(owner=user, id=id)
        except cls.DoesNotExist:
            return None

        return instance

    @classmethod
    def get_by_category(cls, user, category):
        """
        Get diary notes by category

        Args:
            user (User): User object
            category (Category): Category object

        Returns:
            QuerySet: QuerySet of DiaryNote objects

        """
        return cls.objects.filter(owner=user, category=category).select_related(
            "owner", "category"
        )

    @classmethod
    def get_by_priority(cls, user, priority):
        """
        Get diary notes by priority

        Args:
            user (User): User object
            priority (str): priority level

        Returns:
            QuerySet: QuerySet of DiaryNote objects

        """
        return cls.objects.filter(owner=user, priority=priority).select_related(
            "owner", "category"
        )

    @classmethod
    def get_by_due_date(cls, user, date):
        """
        Get diary notes by due date

        Args:
            user (User): User object
            date (date): date

        Returns:
            QuerySet: QuerySet of DiaryNote objects

        """
        return cls.objects.filter(owner=user, due_date=date).select_related(
            "owner", "category"
        )

    @classmethod
    def get_by_is_finished(cls, user, is_finished):
        """
        Get diary notes by is_finished

        Args:
            user (User): User object
            is_finished (bool): is_finished

        Returns:
            QuerySet: QuerySet of DiaryNote objects

        """
        return cls.objects.filter(owner=user, is_finished=is_finished).select_related(
            "owner", "category"
        )

    @classmethod
    def fetched_due_notes(cls, user):
        """
        Get fetched due diary notes

        Args:
            user (User): User object

        Returns:
            QuerySet: QuerySet of DiaryNote objects

        """
        return cls.objects.filter(owner=user, due=True).select_related(
            "owner", "category"
        )

    @classmethod
    def get_unfinished(cls, user):
        """
        Get unfinished diary notes

        Args:
            user (User): User object

        Returns:
            QuerySet: QuerySet of DiaryNote objects

        """
        return cls.objects.filter(owner=user, is_finished=False).select_related(
            "owner", "category"
        )

    @classmethod
    def create_note(cls, **kwargs):
        """
        Create a diary note

        kwargs:
            owner (User): User object
            title (str): title
            content (str): content
            category (Category): Category object
            priority (str): priority level
            due_date (date): due date
            is_finished (bool): is_finished

        Returns:
            DiaryNote: DiaryNote object

        """
        return cls.objects.create(**kwargs)


class NoteReminder(BaseModel):
    REMINDER_INTERVALS = (
        ("Thirty_Minutes", "Thirty Minutes"),
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
        ("Yearly", "Yearly"),
    )

    note = models.ForeignKey(DiaryNote, on_delete=models.CASCADE)
    start_date = models.DateField()
    reminder_interval = models.CharField(max_length=100, choices=REMINDER_INTERVALS)
    reminder_message = models.TextField()

    def __str__(self):
        return self.note.title

    class Meta:
        verbose_name = "NOTE REMINDER"
        verbose_name_plural = "NOTE REMINDERS"
