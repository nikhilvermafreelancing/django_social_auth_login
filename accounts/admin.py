from django.contrib import admin

from accounts.models import CustomUser


# Register your models here.

@admin.register(CustomUser)
class UserAdminView(admin.ModelAdmin):
    list_display = ('id', 'email',)