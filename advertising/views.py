from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import socket
from advertising.forms import LettersForm
from advertising.models import Subscribers, Letters


class SubscriberCreateView(View):
    model = Subscribers
    success_url = reverse_lazy('main:info')

    def post(self, request):
        email_input = request.POST.get("email_field")
        if not Subscribers.objects.filter(email=email_input):
            Subscribers.objects.create(email=email_input)
        return redirect('main:info')


class LettersCreateView(LoginRequiredMixin, CreateView):
    model = Letters
    form_class = LettersForm
    template_name = 'advertising/letters_form.html'
    success_url = reverse_lazy('ad:letters-create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["letters"] = Letters.objects.all()
        return context


class LettersUpdateView(LoginRequiredMixin, UpdateView):
    model = Letters
    form_class = LettersForm
    success_url = reverse_lazy('ad:letters-create')
    template_name = 'advertising/letters_form.html'

    def get_success_url(self):
        return reverse('ad:letters-create')

    def test_func(self):
        result = self.request.user.groups.filter(name='promotioner').exists() or self.request.user.is_superuser
        return result


class LettersDeleteView(LoginRequiredMixin, DeleteView):
    model = Letters
    success_url = reverse_lazy('ad:letters-create')
    template_name = 'advertising/letters_confirm_delete.html'

    def test_func(self):
        result = self.request.user.groups.filter(name='promotioner').exists() or self.request.user.is_superuser
        return result


class SendLetterView(LoginRequiredMixin, View):
    model = Letters

    def post(self, request, pk):
        if self.request.user.is_staff:
            socket.getaddrinfo('localhost', 8001)
            letter = Letters.objects.get(pk=pk)
            recipient_list = list(Subscribers.objects.values_list('email', flat=True))
            send_mail(
                subject=letter.subject,
                message=letter.message,
                from_email=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
                recipient_list=recipient_list
            )

            return HttpResponseRedirect(reverse_lazy('ad:letters-create'))

    def test_func(self):
        result = self.request.user.groups.filter(name='promotioner').exists() or self.request.user.is_superuser
        return result
