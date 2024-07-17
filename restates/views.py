from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login
from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages

from accounts.models import CustomUserModel
from accounts.forms import RegistrationForm
from accounts.checkers import send_otp, get_random_otp, otp_time_checker

from .models import SaleFile, RentFile, City, District, TradeSession
from .forms import SaleFileCreateForm, SaleFileFilterForm, RentFileCreateForm, RentFileFilterForm, TradeSessionForm


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


# --------------------------------- Sale Files ---------------------------------
class SaleFileCreateView(CreateView):
    model = SaleFile
    form_class = SaleFileCreateForm
    template_name = 'restates/sale_file_create.html'

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


class SaleFileDetailView(DetailView):
    model = SaleFile
    context_object_name = 'sale_file'
    template_name = 'restates/sale_file_detail.html'


class SaleFileListView(ListView):
    model = SaleFile
    template_name = 'restates/sale_file_list.html'
    context_object_name = 'sale_files'
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
            # queryset_final = queryset_filtered
            if form.cleaned_data['min_price']:
                queryset_filtered = queryset_filtered.filter(price__gte=form.cleaned_data['min_price'])
            if form.cleaned_data['max_price']:
                queryset_filtered = queryset_filtered.filter(price__lte=form.cleaned_data['max_price'])
            if form.cleaned_data['min_area']:
                queryset_filtered = queryset_filtered.filter(area__gte=form.cleaned_data['min_area'])
            if form.cleaned_data['max_area']:
                queryset_filtered = queryset_filtered.filter(area__lte=form.cleaned_data['max_area'])
            if form.cleaned_data['min_room']:
                queryset_filtered = queryset_filtered.filter(room__gte=int(form.cleaned_data['min_room']))
            if form.cleaned_data['max_room']:
                queryset_filtered = queryset_filtered.filter(room__lte=int(form.cleaned_data['max_room']))
            if form.cleaned_data['min_age']:
                queryset_filtered = queryset_filtered.filter(age__gte=int(form.cleaned_data['min_age']))
            if form.cleaned_data['max_age']:
                queryset_filtered = queryset_filtered.filter(age__lte=int(form.cleaned_data['max_age']))
            if form.cleaned_data['min_level']:
                queryset_filtered = queryset_filtered.filter(level__gte=int(form.cleaned_data['min_level']))
            if form.cleaned_data['max_level']:
                queryset_filtered = queryset_filtered.filter(level__lte=int(form.cleaned_data['max_level']))
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


# --------------------------------- Rent Files ---------------------------------
class RentFileCreateView(CreateView):
    model = RentFile
    form_class = RentFileCreateForm
    template_name = 'restates/rent_file_create.html'

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


class RentFileDetailView(DetailView):
    model = RentFile
    context_object_name = 'rent_file'
    template_name = 'restates/rent_file_detail.html'


class RentFileListView(ListView):
    model = RentFile
    template_name = 'restates/rent_file_list.html'
    context_object_name = 'rent_files'
    paginate_by = 6

    def get_queryset(self):
        queryset_default = RentFile.objects.select_related('province', 'city', 'district')
        form = RentFileFilterForm(self.request.GET)

        if form.is_valid():
            queryset_filtered = queryset_default
            if form.cleaned_data['province']:
                queryset_filtered = queryset_filtered.filter(province=form.cleaned_data['province'])
            if form.cleaned_data['city']:
                queryset_filtered = queryset_filtered.filter(city=form.cleaned_data['city'])
            if form.cleaned_data['district']:
                queryset_filtered = queryset_filtered.filter(district=form.cleaned_data['district'])
            # queryset_final = queryset_filtered
            if form.cleaned_data['min_price_deposit']:
                queryset_filtered = queryset_filtered.filter(price__gte=form.cleaned_data['min_price_deposit'])
            if form.cleaned_data['max_price_deposit']:
                queryset_filtered = queryset_filtered.filter(price__lte=form.cleaned_data['max_price_deposit'])
            if form.cleaned_data['min_price_rent']:
                queryset_filtered = queryset_filtered.filter(price__gte=form.cleaned_data['min_price_rent'])
            if form.cleaned_data['max_price_rent']:
                queryset_filtered = queryset_filtered.filter(price__lte=form.cleaned_data['max_price_rent'])
            if form.cleaned_data['min_area']:
                queryset_filtered = queryset_filtered.filter(area__gte=form.cleaned_data['min_area'])
            if form.cleaned_data['max_area']:
                queryset_filtered = queryset_filtered.filter(area__lte=form.cleaned_data['max_area'])
            if form.cleaned_data['min_room']:
                queryset_filtered = queryset_filtered.filter(room__gte=int(form.cleaned_data['min_room']))
            if form.cleaned_data['max_room']:
                queryset_filtered = queryset_filtered.filter(room__lte=int(form.cleaned_data['max_room']))
            if form.cleaned_data['min_age']:
                queryset_filtered = queryset_filtered.filter(age__gte=int(form.cleaned_data['min_age']))
            if form.cleaned_data['max_age']:
                queryset_filtered = queryset_filtered.filter(age__lte=int(form.cleaned_data['max_age']))
            if form.cleaned_data['min_level']:
                queryset_filtered = queryset_filtered.filter(level__gte=int(form.cleaned_data['min_level']))
            if form.cleaned_data['max_level']:
                queryset_filtered = queryset_filtered.filter(level__lte=int(form.cleaned_data['max_level']))
            return queryset_filtered
        return queryset_default

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RentFileFilterForm(self.request.GET)

        if self.request.GET.get('province'):
            form.fields['city'].queryset = City.objects.filter(province_id=self.request.GET.get('province'))
        if self.request.GET.get('city'):
            form.fields['district'].queryset = District.objects.filter(city_id=self.request.GET.get('city'))

        context['filter_form'] = form
        return context


# --------------------------------- Trades ---------------------------------
def trade_session_view(request):
    if request.method == 'POST':
        form = TradeSessionForm(request.POST)
        if form.is_valid():
            trade_session = form.save(commit=False)
            if request.POST.get('sale_code') != '':
                sale_code = request.POST.get('sale_code')
                sale_file = SaleFile.objects.get(code=sale_code)
                # form.sale_file = sale_file
                trade_session.sale_file = sale_file
            if request.POST.get('rent_code') != '':
                rent_code = request.POST.get('rent_code')
                rent_file = RentFile.objects.get(code=rent_code)
                # form.rent_file = rent_file
                trade_session.rent_file = rent_file
            trade_session.save()
            context = {
                'form': form,
            }
            return HttpResponseRedirect(reverse('trade_session_registration'))
    else:
        form = TradeSessionForm()
    return render(request, 'restates/trade_session.html', {'form': form})


def trade_session_registration_view(request):
    form = RegistrationForm
    if request.method == 'POST':
        try:
            if 'phone_number' in request.POST:
                phone_number = request.POST.get('phone_number')
                user = CustomUserModel.objects.get(phone_number=phone_number)
                if user.otp_code is not None and otp_time_checker(user.phone_number):
                    request.session['user_phone_number'] = user.phone_number
                    print('pussy pussy pussy pussy')
                    return HttpResponseRedirect(reverse('trade_session_verification'))
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.save()
                request.session['user_phone_number'] = user.phone_number
                print('dick dick dick dick')
                return HttpResponseRedirect(reverse('trade_session_verification'))
        except CustomUserModel.DoesNotExist:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.is_active = False
                user.save()
                request.session['user_phone_number'] = user.phone_number
                print('nipple nipple nipple nipple')
                return HttpResponseRedirect(reverse('trade_session_verification'))
    context = {
        'form': form,
    }
    return render(request, 'restates/trade_session_registration.html', context)


def trade_session_verification_view(request):
    try:
        trade_session = TradeSession.objects.get(id=TradeSession.objects.last().id)
        phone_number = request.session.get('user_phone_number')
        user = CustomUserModel.objects.get(phone_number=phone_number)
        if request.method == 'POST':
            if not otp_time_checker(user.phone_number) or user.otp_code != int(request.POST.get('otp')):
                return HttpResponseRedirect(reverse('trade_session_registration'))
            user.is_active = True
            trade_session.phone_number = user.phone_number
            trade_session.save()
            user.save()
            login(request, user)
            return redirect('trade_session_detail', pk=trade_session.pk)
        context = {
            'phone_number': phone_number,
        }
        return render(request, 'restates/trade_session_verification.html', context)
    except CustomUserModel.DoesNotExist:
        return HttpResponseRedirect(reverse('trade_session_registration'))


def trade_session_detail(request, pk):
    # trade_session = get_object_or_404(TradeSession, pk=pk)
    trade_session = TradeSession.objects.select_related('rent_file', 'sale_file').get(pk=pk)
    title = trade_session.rent_file
    print(title)
    context = {
        'trade_session': trade_session,
    }
    return render(request, 'restates/trade_session_detail.html', context)

