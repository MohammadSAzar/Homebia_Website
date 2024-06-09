from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, CreateView, ListView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from .models import SaleFile, City, District
from .forms import SaleFileCreateForm, create_file_fields
from . import checkers

def real_estate_create(request):
    if request.method == 'POST':
        form = SaleFileCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SaleFileCreateForm()
    return render(request, 'files/file_create.html', {'form': form})


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
    template_name = 'files/file_detail.html'

class SaleFileListView(ListView):
    model = SaleFile
    paginate_by = 6
    context_object_name = 'files'
    template_name = 'files/file_list.html'

