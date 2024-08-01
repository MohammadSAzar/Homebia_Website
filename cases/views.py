from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, DetailView

from .models import Case, CaseOrder, CaseOrderItem, Province, City, District
from .forms import CaseFilterForm, AddToCartForm, OrderForm
from .cart import Cart


# --------------------------------- Locations ---------------------------------
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


def load_cities_list(request):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse({'cities': list(cities)})


def load_districts_list(request):
    city_id = request.GET.get('city_id')
    districts = District.objects.filter(city_id=city_id).values('id', 'name')
    return JsonResponse({'districts': list(districts)})


# --------------------------------- Case Views ---------------------------------
class CaseListView(ListView):
    model = Case
    paginate_by = 8
    context_object_name = 'cases'
    template_name = 'cases/case_list.html'

    def get_queryset(self):
        queryset_default = Case.objects.select_related('province', 'city', 'district')
        form = CaseFilterForm(self.request.GET)

        if form.is_valid():
            queryset_filtered = queryset_default
            if form.cleaned_data['province']:
                queryset_filtered = queryset_filtered.filter(province=form.cleaned_data['province'])
            if form.cleaned_data['city']:
                queryset_filtered = queryset_filtered.filter(city=form.cleaned_data['city'])
            if form.cleaned_data['district']:
                queryset_filtered = queryset_filtered.filter(district=form.cleaned_data['district'])
            if form.cleaned_data['min_metric_price']:
                queryset_filtered = queryset_filtered.filter(metric_price__gte=form.cleaned_data['min_metric_price'])
            if form.cleaned_data['max_metric_price']:
                queryset_filtered = queryset_filtered.filter(metric_price__lte=form.cleaned_data['max_metric_price'])
            return queryset_filtered
        return queryset_default

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CaseFilterForm(self.request.GET)

        if self.request.GET.get('province'):
            form.fields['city'].queryset = City.objects.filter(province_id=self.request.GET.get('province'))
        if self.request.GET.get('city'):
            form.fields['district'].queryset = District.objects.filter(city_id=self.request.GET.get('city'))

        context['filter_form'] = form
        return context


class CaseDetailView(DetailView):
    model = Case
    template_name = 'cases/case_detail.html'
    context_object_name = 'case'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_to_cart_form'] = AddToCartForm()
        return context


# --------------------------------- Cart Views ---------------------------------
def cart_detail_view(request):
    order_form = OrderForm()
    cart = Cart(request)

    for item in cart:
        item['case_update_meter_form'] = AddToCartForm(initial={
            'meter': item['meter'],
            'inplace': True,
        })

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                case = item['case_obj']
                CaseOrderItem.objects.create(
                    order=order_obj,
                    case=case,
                    meter=item['meter'],
                )
            cart.clear()
            return redirect('case_list')

    context = {
        'cart': cart,
        'order_form': order_form,
    }
    return render(request, 'cases/cart_detail.html', context)


def add_to_cart_view(request, case_id):
    cart = Cart(request)
    case = get_object_or_404(Case, id=case_id)
    form = AddToCartForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        meter = cleaned_data['meter']
        cart.add(case, meter, replace_current_meter=cleaned_data['inplace'])
    return redirect('cart_detail')


def remove_from_cart_view(request, case_id):
    cart = Cart(request)
    case = get_object_or_404(Case, id=case_id)
    cart.remove(case)
    return redirect('cart_detail')


@require_POST
def cart_clear(request):
    cart = Cart(request)
    if len(cart):
        cart.clear()
        messages.success(request, 'سبد با موفقیت خالی شد')
    else:
        messages.warning(request, 'سبد شما خالی است')
    return redirect('cart_empty')


def cart_empty_view(request):
    return render(request, 'cases/cart_empty.html')




