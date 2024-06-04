from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import CreateView, DetailView, CreateView
from django.shortcuts import render

from .models import File, City, District
from .forms import FileCreateForm, create_file_fields


def real_estate_create(request):
    if request.method == 'POST':
        form = FileCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page or any desired URL
    else:
        form = FileCreateForm()
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


