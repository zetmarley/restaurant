from django.urls import path
from django.views.decorators.cache import cache_page
from main import views
from main.apps import MainConfig
from main.views import TableListView, TableCreateView, TableUpdateView, TableDeleteView, \
    BookingCreateView, BookingListView, BookingUpdateView, BookingDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(0)(views.info), name='info'),
    path('menu/', cache_page(0)(views.menu), name='menu'),
    # CRUD Столов без detail
    path('table/create/', cache_page(60)(TableCreateView.as_view()), name='table-create'),
    path('table/', cache_page(0)(TableListView.as_view()), name='table-list'),
    path('table/update/<int:pk>/', cache_page(60)(TableUpdateView.as_view()), name='table-update'),
    path('table/delete/<int:pk>/', cache_page(60)(TableDeleteView.as_view()), name='table-delete'),
    # CRUD Бронь без detail
    path('booking/create/', cache_page(0)(BookingCreateView.as_view()), name='booking-create'),
    path('booking/', cache_page(0)(BookingListView.as_view()), name='booking-list'),
    path('booking/update/<int:pk>/', cache_page(60)(BookingUpdateView.as_view()), name='booking-update'),
    path('booking/delete/<int:pk>/', cache_page(60)(BookingDeleteView.as_view()), name='booking-delete'),
]
