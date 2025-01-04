from django.contrib import admin
from advertising.models import Subscribers


@admin.register(Subscribers)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email',)
    search_fields = ('id', 'name', 'phone', 'email',)