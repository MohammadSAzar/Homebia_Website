from django.shortcuts import reverse
from django.views.generic import CreateView, DetailView, CreateView, ListView
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages

from .models import SaleFile, City, District
from .forms import SaleFileCreateForm, SaleFileFilterForm


class SaleFileCreateView(CreateView):
    model = SaleFile
    form_class = SaleFileCreateForm
    template_name = 'restates/file_create.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "آگهی شما پس از تایید ادمین در سایت منتشر خواهد شد.")
        return super().form_valid(form)

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
    template_name = 'restates/file_list.html'
    context_object_name = 'files'
    paginate_by = 6

    def get_queryset(self):
        queryset_default = SaleFile.objects.select_related('province', 'city', 'district')
        form = SaleFileFilterForm(self.request.GET)

        if form.is_valid():
            queryset_filtered = queryset_default
            if form.cleaned_data['province']:
                queryset_filtered = queryset_filtered.filter(province=form.cleaned_data['province'])
            if form.cleaned_data['city']:
                queryset_filtered = queryset_filtered.filter(city=form.cleaned_data['city'])
            if form.cleaned_data['district']:
                queryset_filtered = queryset_filtered.filter(district=form.cleaned_data['district'])
            return queryset_filtered
        return queryset_default

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SaleFileFilterForm(self.request.GET)

        if self.request.GET.get('province'):
            form.fields['city'].queryset = City.objects.filter(province_id=self.request.GET.get('province'))
        if self.request.GET.get('city'):
            form.fields['district'].queryset = District.objects.filter(city_id=self.request.GET.get('city'))

        context['filter_form'] = form
        return context


def load_cities_list(request):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse({'cities': list(cities)})

def load_districts_list(request):
    city_id = request.GET.get('city_id')
    districts = District.objects.filter(city_id=city_id).values('id', 'name')
    return JsonResponse({'districts': list(districts)})






