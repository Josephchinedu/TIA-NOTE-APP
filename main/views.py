from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main.helpers.pagination_helper import CustomPagination
from main.models import Category, DiaryNote, NoteReminder
from main.serializers import (
    CategorySerializer,
    CreateDiaryNoteSerializer,
    CreateReminderSerializer,
    DiaryNoteSerializer,
    DownloadNoteSerializer,
    NoteReminderSerializer,
    UpdateReminderSerializer,
)
from main.tasks import celery_send_diary_note_as_a_file

# Create your views here.


class NoteCategoryApiView(APIView):
    """
    NOTE CATEGORY API VIEW
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CategorySerializer

    # swagger schema
    fetch_category_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "created_at": openapi.Schema(type=openapi.TYPE_STRING),
            "updated_at": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )

    fetch_category_response_schema = {
        "200": openapi.Response(
            description="Category fetched successfully",
            schema=fetch_category_schema,
        ),
        "400": "Bad Request",
        "401": "Unauthorized",
        "403": "Forbidden",
    }

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["category"],
        operation_description="Category",
        responses=fetch_category_response_schema,
    )
    def get(self, request):
        """
        GET REQUEST
        """
        category_qs = Category.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(category_qs, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class DiaryNoteApiView(APIView):
    """
    DIARY NOTE API VIEW
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # CREATE NOTE SWAGGER SCHEMA
    create_note_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(type=openapi.TYPE_STRING),
            "content": openapi.Schema(type=openapi.TYPE_STRING),
            "category": openapi.Schema(type=openapi.TYPE_INTEGER),
            "priority": openapi.Schema(type=openapi.TYPE_STRING),
            "due_date": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["title", "content", "category", "priority", "due_date"],
    )

    create_note_response_schema = {
        status.HTTP_201_CREATED: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "content": openapi.Schema(type=openapi.TYPE_STRING),
                "category": openapi.Schema(type=openapi.TYPE_INTEGER),
                "priority": openapi.Schema(type=openapi.TYPE_STRING),
                "due_date": openapi.Schema(type=openapi.TYPE_STRING),
                "is_finished": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                "updated_at": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    }

    # end of create note swagger schema

    # UPDATE NOTE SWAGGER SCHEMA

    update_note_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(type=openapi.TYPE_STRING),
            "content": openapi.Schema(type=openapi.TYPE_STRING),
            "category": openapi.Schema(type=openapi.TYPE_INTEGER),
            "priority": openapi.Schema(type=openapi.TYPE_STRING),
            "due_date": openapi.Schema(type=openapi.TYPE_STRING),
            "is_finished": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        },
        required=["title", "content", "category", "priority", "due_date"],
    )

    update_note_response_schema = {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "content": openapi.Schema(type=openapi.TYPE_STRING),
                "category": openapi.Schema(type=openapi.TYPE_INTEGER),
                "priority": openapi.Schema(type=openapi.TYPE_STRING),
                "due_date": openapi.Schema(type=openapi.TYPE_STRING),
                "is_finished": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                "updated_at": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    }

    # end of update note swagger schema

    # partial update note swagger schema

    partial_update_note_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(type=openapi.TYPE_STRING),
            "content": openapi.Schema(type=openapi.TYPE_STRING),
            "category": openapi.Schema(type=openapi.TYPE_INTEGER),
            "priority": openapi.Schema(type=openapi.TYPE_STRING),
            "due_date": openapi.Schema(type=openapi.TYPE_STRING),
            "is_finished": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        },
    )

    partial_update_note_response_schema = {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "content": openapi.Schema(type=openapi.TYPE_STRING),
                "category": openapi.Schema(type=openapi.TYPE_INTEGER),
                "priority": openapi.Schema(type=openapi.TYPE_STRING),
                "due_date": openapi.Schema(type=openapi.TYPE_STRING),
                "is_finished": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                "updated_at": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    }

    # end of partial update note swagger schema

    # delete note swagger schema

    delete_note_response_schema = {
        status.HTTP_204_NO_CONTENT: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    }

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["diary-note"],
        operation_description="Create Diary Note",
        request_body=create_note_schema,
    )
    def post(self, request):
        serializer = CreateDiaryNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get category object
        try:
            category = Category.objects.get(
                id=serializer.validated_data.get("category")
            )
        except Category.DoesNotExist:
            return Response(
                {"message": "Category does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # create diary note object
        payload = {
            "owner": request.user,
            "title": serializer.validated_data.get("title"),
            "content": serializer.validated_data.get("content"),
            "category": category,
            "priority": serializer.validated_data.get("priority_level"),
            "due_date": serializer.validated_data.get("due_date"),
        }

        note = DiaryNote.create_note(
            **payload,
        )

        data = DiaryNoteSerializer(note).data

        return Response(data, status=status.HTTP_201_CREATED)

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["diary-note"],
        operation_description="Get Diary Note",
        responses=create_note_response_schema,
    )
    def get(self, request):
        """
        THIS METHOD ALLOW USERS TO GET A DIARY NOTE

        DESCRIPTION:
            - This method allow users to get a diary note by providing the note id
            - This method also allow users to filter their diary notes by providing the filter_by query parameter
            - The filter_by query parameter can be one of the following: unfinished, overdue, done
            - If the filter_by query parameter is not provided, all diary notes will be returned
            - This method also allow users to sort their diary notes by providing the sort_by query parameter
            - The sort_by query parameter can be one of the following: due_date, priority, created_time
        """
        filter_options = ["unfinished", "overdue", "done"]
        sort_options = ["due_date", "priority", "created_date"]

        sort_by = request.GET.get("sort_by", None)

        filter_by = request.GET.get("filter_by", None)
        if filter_by is not None:
            if filter_by not in filter_options:
                return Response(
                    {"message": "Invalid filter option"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if filter_by == "unfinished":
                user_notes = DiaryNote.get_unfinished(user=request.user)

            elif filter_by == "overdue":
                user_notes = DiaryNote.fetched_due_notes(user=request.user)
            elif filter_by == "done":
                user_notes = DiaryNote.get_by_is_finished(
                    user=request.user, is_finished=True
                )

            else:
                user_notes = DiaryNote.get_all(user=request.user)

        else:
            user_notes = DiaryNote.get_all(user=request.user)

        # sort queryset section
        if sort_by is not None:
            if sort_by not in sort_options:
                return Response(
                    {"message": "Invalid sort option"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if sort_by == "due_date":
                user_notes = user_notes.order_by("due_date")
            elif sort_by == "priority":
                user_notes = user_notes.order_by("priority")
            elif sort_by == "created_date":
                user_notes = user_notes.order_by("created_at")

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(user_notes, request)
        serializer = DiaryNoteSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["diary-note"],
        operation_description="Update Diary Note",
        request_body=update_note_schema,
        responses=update_note_response_schema,
    )
    def put(self, request):
        """
        THIS METHOD ALLOW USERS TO UPDATE A DIARY NOTE

        """

        note_id = request.GET.get("note_id", None)

        if note_id is None:
            return Response(
                {"message": "Note ID is required to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CreateDiaryNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        priority_level = serializer.validated_data.get("priority_level")
        category = serializer.validated_data.get("category")

        try:
            category = Category.objects.get(id=category)
        except Category.DoesNotExist:
            return Response(
                {"message": "Category does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_note_instance = DiaryNote.get_note_by_id(user=request.user, id=note_id)
        if user_note_instance is None:
            return Response(
                {"message": "Diary Note record not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_note_instance.title = title
        user_note_instance.content = content
        user_note_instance.priority = priority_level
        user_note_instance.category = category
        user_note_instance.save()

        data = DiaryNoteSerializer(user_note_instance).data

        return Response(data, status=status.HTTP_201_CREATED)

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["diary-note"],
        operation_description="Partially Update Diary Note",
        request_body=partial_update_note_schema,
        responses=partial_update_note_response_schema,
    )
    def patch(self, request):
        """
        THIS METHOD ALLOW USERS TO PARTIALLY UPDATE A DIARY NOTE

        """

        note_id = request.GET.get("note_id", None)

        if note_id is None:
            return Response(
                {"message": "Note ID is required to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_note_instance = DiaryNote.get_note_by_id(user=request.user, id=note_id)
        if user_note_instance is None:
            return Response(
                {"message": "Diary Note record not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        title = request.data.get("title", user_note_instance.title)
        content = request.data.get("content", user_note_instance.content)
        priority_level = request.data.get("priority_level", user_note_instance.priority)
        category = request.data.get("category", None)

        try:
            if category is None:
                category = user_note_instance.category
            else:
                category = Category.objects.get(id=category)
        except Category.DoesNotExist:
            return Response(
                {"message": "Category does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_note_instance.title = title
        user_note_instance.content = content
        user_note_instance.priority = priority_level
        user_note_instance.category = category
        user_note_instance.save()

        data = DiaryNoteSerializer(user_note_instance).data

        return Response(data, status=status.HTTP_201_CREATED)

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["diary-note"],
        operation_description="Delete Diary Note",
        responses=delete_note_response_schema,
    )
    def delete(self, request):
        """
        THIS METHOD ALLOW USERS TO DELETE A DIARY NOTE

        """

        note_id = request.GET.get("note_id", None)

        if note_id is None:
            return Response(
                {"message": "Note ID is required to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_note_instance = DiaryNote.get_note_by_id(user=request.user, id=note_id)
        if user_note_instance is None:
            return Response(
                {"message": "Diary Note record not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_note_instance.delete()

        return Response(
            {"message": "Diary note deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class DownloadNoteToFile(APIView):
    """
    DOWNLOAD NOTE TO FILE API VIEW
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    download_note_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "note_ids": openapi.Schema(
                type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
            ),
            "file_type": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["note_ids", "file_type"],
    )

    download_note_response_schema = {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    }

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["download"],
        operation_description="Create Diary Note",
    )
    def get(self, request):
        users_notes = DiaryNote.get_all(user=request.user)
        note_ids = list(users_notes.values_list("id", flat=True))

        print("note_ids", note_ids, "\n\n\n")

        file_type_options = ["pdf", "csv"]
        file_type = request.GET.get("file_type", None)

        if file_type not in file_type_options:
            return Response(
                {"message": "invalid file type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        celery_send_diary_note_as_a_file.delay(
            item_ids=note_ids,
            email=request.user.email,
            file_type=file_type,
            name=request.user.first_name,
        )

        return Response(
            {
                "message": "request recieved, you'll get email notification when your file is ready."
            },
            status=status.HTTP_200_OK,
        )

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["download"],
        operation_description="Create Diary Note",
        request_body=download_note_schema,
        responses=download_note_response_schema,
    )
    def post(self, request):
        serializer = DownloadNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note_ids = serializer.validated_data.get("note_ids")
        file_type = serializer.validated_data.get("file_type")

        celery_send_diary_note_as_a_file(
            item_ids=note_ids,
            email=request.user.email,
            file_type=file_type,
            name=request.user.first_name,
        )

        return Response(
            {
                "message": "request recieved, you'll get email notification when your file is ready."
            },
            status=status.HTTP_200_OK,
        )


class NoteReminderApiView(APIView):
    """
    NOTE REMINDER API VIEW
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # CREATE NOTE REMINDER SWAGGER SCHEMA

    create_note_reminder_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "note_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "start_date": openapi.Schema(type=openapi.TYPE_STRING),
            "reminder_interval": openapi.Schema(type=openapi.TYPE_STRING),
            "reminder_message": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["note_id", "start_date", "reminder_interval", "reminder_message"],
    )

    create_note_reminder_response_schema = {
        status.HTTP_201_CREATED: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "note": openapi.Schema(type=openapi.TYPE_INTEGER),
                "start_date": openapi.Schema(type=openapi.TYPE_STRING),
                "reminder_interval": openapi.Schema(type=openapi.TYPE_STRING),
                "reminder_message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    }

    # end of create note reminder swagger schema

    # update note reminder swagger schema

    update_note_reminder_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "note_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "start_date": openapi.Schema(type=openapi.TYPE_STRING),
            "reminder_interval": openapi.Schema(type=openapi.TYPE_STRING),
            "reminder_message": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["note_id", "start_date", "reminder_interval", "reminder_message"],
    )

    update_note_reminder_response_schema = {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "note": openapi.Schema(type=openapi.TYPE_INTEGER),
                "start_date": openapi.Schema(type=openapi.TYPE_STRING),
                "reminder_interval": openapi.Schema(type=openapi.TYPE_STRING),
                "reminder_message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    }

    # end of update note reminder swagger schema

    # delete note reminder swagger schema

    delete_note_reminder_response_schema = {
        status.HTTP_204_NO_CONTENT: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    }

    # end of delete note reminder swagger schema

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["note-reminder"],
        operation_description="Create Note Reminder",
        request_body=create_note_reminder_schema,
        responses=create_note_reminder_response_schema,
    )
    def post(self, request):
        serializer = CreateReminderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note_id = serializer.validated_data.get("note_id")
        start_date = serializer.validated_data.get("start_date")
        reminder_interval = serializer.validated_data.get("reminder_interval")
        reminder_message = serializer.validated_data.get("reminder_message")

        try:
            note = DiaryNote.objects.get(id=note_id, owner=request.user)
        except DiaryNote.DoesNotExist:
            return Response(
                {"message": "Diary Note does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload = {
            "note": note,
            "start_date": start_date,
            "reminder_interval": reminder_interval,
            "reminder_message": reminder_message,
        }

        note_reminder = NoteReminder.objects.create(**payload)

        data = NoteReminderSerializer(note_reminder).data

        return Response(data, status=status.HTTP_201_CREATED)

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["note-reminder"],
        operation_description="Update Note Reminder",
        request_body=update_note_reminder_schema,
        responses=update_note_reminder_response_schema,
    )
    def put(self, request):
        serializer = UpdateReminderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data.get("start_date")
        reminder_interval = serializer.validated_data.get("reminder_interval")
        reminder_message = serializer.validated_data.get("reminder_message")

        note_reminder_id = request.GET.get("note_reminder_id", None)

        try:
            note_reminder = NoteReminder.objects.get(id=note_reminder_id)
        except NoteReminder.DoesNotExist:
            return Response(
                {"message": "Note reminder does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        note_reminder.start_date = start_date
        note_reminder.reminder_interval = reminder_interval
        note_reminder.reminder_message = reminder_message
        note_reminder.save()

        data = NoteReminderSerializer(note_reminder).data

        return Response(data, status=status.HTTP_201_CREATED)

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        tags=["note-reminder"],
        operation_description="Delete Note Reminder",
        responses=delete_note_reminder_response_schema,
    )
    def delete(self, request):
        note_id = request.GET.get("note_reminder_id", None)

        if note_id is None:
            return Response(
                {"message": "Note ID is required to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            note = NoteReminder.objects.get(
                id=note_id,
            )
        except NoteReminder.DoesNotExist:
            return Response(
                {"message": "Note reminder does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        note.delete()

        return Response(
            {"message": "Note reminder deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
