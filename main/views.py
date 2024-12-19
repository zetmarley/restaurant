from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from config.settings import BASE_DIR
from main.forms import BookingForm
# from main.forms import ProductForm, VersionForm, ProductFormForModerator
from main.models import Table, Booking
from django.views.generic.list import ListView

# from main.services import get_cached_categories_for_product

def info(request):
    return render(request, f"{BASE_DIR}/main/templates/info.html")


class TableListView(ListView):
    model = Table
    template_name = 'booking_form.html'


class TableDetailView(LoginRequiredMixin, DetailView):
    model = Table
    template_name = 'table_info.html'


class TableCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Table
    # form_class = ProductForm
    permission_required = 'main.add_table'
    success_url = reverse_lazy('main:list')
    template_name = 'table_form.html'


class TableUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Table
    # form_class = ProductForm
    permission_required = 'main.change_table'
    success_url = reverse_lazy('main:list')
    template_name = 'table_form.html'


    def get_success_url(self):
        return reverse('main:info', args=[self.kwargs.get('pk')])

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data()
    #     ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
    #     if self.request.method == 'POST':
    #         context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
    #     else:
    #         context_data['formset'] = ProductFormset(instance=self.object)
    #     return context_data
    #
    # def form_valid(self, form):
    #     context_data = self.get_context_data()
    #     formset = context_data['formset']
    #     if form.is_valid() and formset.is_valid():
    #         self.object = form.save()
    #         formset.instance = self.object
    #         formset.save()
    #         return super().form_valid(form)
    #     else:
    #         raise self.render_to_response(self.get_context_data(form=form, formset=formset))


class TableDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Table
    permission_required = 'main.delete_table'
    success_url = reverse_lazy('main:list')
    template_name = 'table_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('main:booking_create')
    template_name = 'booking_form.html'
    context_object_name = Table

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tables"] = Table.objects.all()
        return context