from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, CreateView, ListView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from .models import SaleFile, City, District
from .forms import SaleFileCreateForm


class SaleFileCreateView(CreateView):
    model = SaleFile
    form_class = SaleFileCreateForm
    template_name = 'restates/file_create.html'

    def post(self, request, *args, **kwargs):
        # form = SaleFileCreateForm(self.request.POST)
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "آگهی شما پس از تایید ادمین در سایت منتشر خواهد شد.")
        return super().form_valid(form)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.save()
    #     return HttpResponseRedirect(reverse('profile_info_now') + '?show_modal=True')

    def form_invalid(self, form):
        self.object = None
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('profile_info_now')


def load_cities(request):
    province_id = request.GET.get('province')
    cities = City.objects.filter(province_id=province_id).order_by('name')
    city_choices = [(city.id, city.name) for city in cities]
    return JsonResponse({'cities': city_choices})


def load_districts(request):
    city_id = request.GET.get('city')
    districts = District.objects.filter(city_id=city_id).order_by('name')
    district_choices = [(district.id, district.name) for district in districts]
    return JsonResponse({'districts': district_choices})


class SaleFileDetailView(DetailView):
    model = SaleFile
    context_object_name = 'sale_file'
    template_name = 'restates/file_detail.html'


class SaleFileListView(ListView):
    model = SaleFile
    paginate_by = 6
    context_object_name = 'files'
    template_name = 'restates/file_list.html'



