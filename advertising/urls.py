from advertising.apps import AdvertisingConfig
from django.urls import path
from advertising.views import SubscriberCreateView, LettersCreateView, LettersUpdateView, LettersDeleteView, \
    SendLetterView

app_name = AdvertisingConfig.name

urlpatterns = [
    path('subscriber/create/', SubscriberCreateView.as_view(), name='subscriber-create'),
    path('letters/create/', LettersCreateView.as_view(), name='letters-create'),
    path('letters/update/<int:pk>/', LettersUpdateView.as_view(), name='letters-update'),
    path('letters/delete/<int:pk>/', LettersDeleteView.as_view(), name='letters-delete'),
    path('letters/send/<int:pk>/', SendLetterView.as_view(), name='send-letter'),
]
