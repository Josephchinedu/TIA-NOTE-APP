from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from account.models import OTP, User

# Register your models here.


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class OTPResource(resources.ModelResource):
    class Meta:
        model = OTP


class UserResourceAdmin(ImportExportModelAdmin):
    resource_class = UserResource

    search_fields = [
        "first_name",
        "last_name",
        "email",
    ]

    list_filter = [
        "created_at",
    ]

    date_hierarchy = "created_at"

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
    

class OTPResourceAdmin(ImportExportModelAdmin):
    resource_class = OTPResource

    search_fields = [
        "recipient"
    ]

    list_filter = [
        "created_at",
    ]

    date_hierarchy = "created_at"

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


admin.site.register(User, UserResourceAdmin)
admin.site.register(OTP, OTPResourceAdmin)
