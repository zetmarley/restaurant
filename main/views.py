from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from advertising.models import Subscribers
from config.settings import BASE_DIR
from main.forms import BookingForm, TableForm, BookingUpdateForm, ContentForm
from main.models import Table, Booking, Content
from django.views.generic.list import ListView


def info(request):
    return render(request, f"{BASE_DIR}/main/templates/info.html")


def menu(request):
    return render(request, f"{BASE_DIR}/main/templates/menu.html")


class ContentListView(ListView):
    model = Content
    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = Content.objects.all()
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context


class TableListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Table
    template_name = 'table_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tables"] = Table.objects.all()
        return context

    def test_func(self):
        result = (self.request.user.groups.filter(name='waiter').exists()
                  or self.request.user.is_superuser or self.request.user.groups.filter(name='observer').exists())
        return result

    # Если проверка не пройдена, выполните перенаправление
    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет доступа к этому ресурсу.")


class TableCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = Table
    form_class = TableForm
    success_url = reverse_lazy('main:table-list')
    template_name = 'table_form.html'

    def test_func(self):
        result = self.request.user.groups.filter(name='waiter').exists() or self.request.user.is_superuser
        return result

    # Если проверка не пройдена, выполните перенаправление
    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет доступа к этому ресурсу.")


class TableUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Table
    form_class = TableForm
    success_url = reverse_lazy('main:table-list')
    template_name = 'table_form.html'

    def test_func(self):
        result = self.request.user.groups.filter(name='waiter').exists() or self.request.user.is_superuser
        return result

    # Если проверка не пройдена, выполните перенаправление
    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет доступа к этому ресурсу.")


class TableDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Table
    success_url = reverse_lazy('main:table-list')
    template_name = 'table_confirm_delete.html'

    def test_func(self):
        result = self.request.user.groups.filter(name='waiter').exists() or self.request.user.is_superuser
        return result

    # Если проверка не пройдена, выполните перенаправление
    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет доступа к этому ресурсу.")


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('main:info')
    template_name = 'booking_form.html'
    context_object_name = Table

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tables"] = Table.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        sub_status = request.POST.get("sub_status")
        if sub_status == 'on':
            client_email = request.POST.get("client_email")
            client_name = request.POST.get("client_name")
            client_phone = request.POST.get("client_phone")

            if Subscribers.objects.filter(email=client_email):
                sub = Subscribers.objects.get(email=client_email)
                sub.phone = client_phone
                sub.name = client_name
                sub.save()
            elif Subscribers.objects.filter(phone=client_phone):
                sub = Subscribers.objects.get(phone=client_phone)
                sub.email = client_email
                sub.name = client_name
                sub.save()
            else:
                Subscribers.objects.create(email=client_email,
                                           phone=client_phone,
                                           name=client_name)

        return super().post(request, *args, **kwargs)


class BookingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Booking
    template_name = 'booking_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bookings"] = Booking.objects.all()
        return context

    def test_func(self):
        result = (self.request.user.groups.filter(name='waiter').exists()
                  or self.request.user.is_superuser or self.request.user.groups.filter(name='observer').exists())
        return result

    # Если проверка не пройдена, выполните перенаправление
    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет доступа к этому ресурсу.")


class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    form_class = BookingUpdateForm
    success_url = reverse_lazy('main:booking-list')
    template_name = 'booking_form.html'

    def test_func(self):
        result = self.request.user.groups.filter(name='waiter').exists() or self.request.user.is_superuser
        return result

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет доступа к этому ресурсу.")


class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('main:booking-list')
    template_name = 'booking_confirm_delete.html'

    def test_func(self):
        result = self.request.user.groups.filter(name='waiter').exists() or self.request.user.is_superuser
        return result

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет доступа к этому ресурсу.")


class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Content
    form_class = ContentForm
    success_url = reverse_lazy('main:info')
    template_name = 'content_form.html'

    def test_func(self):
        result = self.request.user.groups.filter(name='contentmanager').exists() or self.request.user.is_superuser
        return result

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет доступа к этому ресурсу.")


class ContentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Content
    success_url = reverse_lazy('main:info')
    template_name = 'content_confirm_delete.html'

    def test_func(self):
        result = self.request.user.groups.filter(name='contentmanager').exists() or self.request.user.is_superuser
        return result

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет доступа к этому ресурсу.")