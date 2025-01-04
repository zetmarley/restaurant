from advertising.apps import AdvertisingConfig
from django.urls import path
from advertising.views import SubscriberCreateView

app_name = AdvertisingConfig.name

urlpatterns = [
    path('create/', (SubscriberCreateView.as_view()), name='ad-create'),

]
