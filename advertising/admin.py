from django.contrib import admin
from advertising.models import Subscribers, Letters


@admin.register(Subscribers)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email',)
    search_fields = ('id', 'name', 'phone', 'email',)


@admin.register(Letters)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'description',)
    search_fields = ('subject', 'message', 'description',)