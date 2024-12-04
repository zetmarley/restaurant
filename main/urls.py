from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import TableListView, TableDetailView, TableCreateView, TableUpdateView, TableDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(TableListView.as_view()), name='list'),
    path('table/<int:pk>/', cache_page(60)(TableDetailView.as_view()), name='info'),
    path('table/create/', cache_page(60)(TableCreateView.as_view()), name='create'),
    path('table/update/<int:pk>/', cache_page(60)(TableUpdateView.as_view()), name='update'),
    path('table/delete/<int:pk>/', cache_page(60)(TableDeleteView.as_view()), name='delete')
]