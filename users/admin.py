from django.contrib import admin

from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'job_title', 'email', 'phone',)
    search_fields = ('id', 'first_name', 'last_name', 'job_title', 'email', 'phone',)