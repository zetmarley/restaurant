from django.urls import path
from django.views.decorators.cache import cache_page

from main import views
from main.apps import MainConfig
from main.views import TableListView, TableDetailView, TableCreateView, TableUpdateView, TableDeleteView, \
    BookingCreateView

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(0)(views.info), name='info'),
    path('menu/', cache_page(0)(views.menu), name='menu'),
    path('table/create/', cache_page(60)(TableCreateView.as_view()), name='create'),
    path('table/update/<int:pk>/', cache_page(60)(TableUpdateView.as_view()), name='update'),
    path('table/delete/<int:pk>/', cache_page(60)(TableDeleteView.as_view()), name='delete'),
    path('booking/create/', cache_page(60)(BookingCreateView.as_view()), name='booking_create'),
]