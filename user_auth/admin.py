from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserPayment


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("mobile", "created_at")}),
    )
    readonly_fields = ("created_at", "modified_at")


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(UserPayment)
