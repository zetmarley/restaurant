from django.contrib import admin
from main.models import Table, Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'time_from', 'time_to',
                    'client_email', 'client_name', 'client_phone', 'is_notified')
    search_fields = ('table', 'client_email', 'client_phone', 'is_notified')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'free', 'seats', 'is_vip',)
    search_fields = ('id', 'free',)
