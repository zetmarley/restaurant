from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from advertising.models import Subscribers


class SubscriberCreateView(View):
    model = Subscribers
    success_url = reverse_lazy('main:info')

    def post(self, request):
        email_input = request.POST.get("email_field")
        if not Subscribers.objects.filter(email=email_input):
            Subscribers.objects.create(email=email_input)
        return redirect('main:info')