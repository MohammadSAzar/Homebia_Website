from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from .models import AgentCustomUserModel, AgentProfile, Province, City
from accounts.models import CustomUserModel
from .forms import AgentRegistrationForm, AgentInfoCompletionForm, AgentInfoEditForm
from .checkers import send_otp, get_random_otp, otp_time_checker


# --------------------------------- Locations ---------------------------------
def load_cities(request):
    province_id = request.GET.get('province')
    cities = City.objects.filter(province_id=province_id).order_by('name')
    city_choices = [(city.id, city.name) for city in cities]
    return JsonResponse({'cities': city_choices})


def load_cities_list(request):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse({'cities': list(cities)})


# --------------------------------- dashboard ---------------------------------
def agent_registration_view(request):
    form = AgentRegistrationForm
    if request.method == 'POST':
        try:
            if 'phone_number' in request.POST:
                phone_number = request.POST.get('phone_number')
                user = AgentCustomUserModel.objects.get(phone_number=phone_number)
                if user.otp_code is not None and otp_time_checker(user.phone_number):
                    request.session['user_phone_number'] = user.phone_number
                    return HttpResponseRedirect(reverse('agent_verification'))
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.save()
                request.session['user_phone_number'] = user.phone_number
                return HttpResponseRedirect(reverse('agent_verification'))
        except AgentCustomUserModel.DoesNotExist:
            form = AgentRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.is_active = False
                user.save()
                request.session['user_phone_number'] = user.phone_number
                return HttpResponseRedirect(reverse('agent_verification'))
    context = {
        'form': form,
    }
    return render(request, 'agents/agent_registration.html', context)


def agent_verification_view(request):
    try:
        phone_number = request.session.get('user_phone_number')
        user = AgentCustomUserModel.objects.get(phone_number=phone_number)
        if request.method == 'POST':
            if not otp_time_checker(user.phone_number) or user.otp_code != int(request.POST.get('otp')):
                return HttpResponseRedirect(reverse('agent_verification'))
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('agent_profile_info_now'))
        context = {
            'phone_number': phone_number,
        }
        return render(request, 'agents/agent_verification.html', context)
    except AgentCustomUserModel.DoesNotExist:
        return HttpResponseRedirect(reverse('agent_registration'))


def agent_profile_info_now(request):
    context = {}
    phone_number = request.session.get('user_phone_number')
    if phone_number:
        try:
            agent_user = AgentCustomUserModel.objects.get(phone_number=phone_number)
            context['agent_user'] = agent_user
            print('ASS')

            if request.method == 'POST':
                if agent_user.complete_info == 'dnt':
                    form = AgentInfoCompletionForm(request.POST)
                    if form.is_valid():
                        agent_profile = form.save(commit=False)
                        agent_profile.agent = agent_user
                        agent_profile.save()
                        form.save()
                        agent_user.complete_info = 'ipr'
                        agent_user.save()
                        messages.success(request, "اطلاعات شما دریافت شد، نتیجه بررسی آن بزودی تعیین می‌شود.")
                        return HttpResponseRedirect(reverse('agent_profile_info_now'))
                else:
                    form = AgentInfoEditForm(request.POST)
                    agent_profile = AgentProfile.objects.get(agent=agent_user)
                    if form.is_valid():
                        form.save()
                        agent_profile.save()
                        agent_user.complete_info = 'ipr'
                        agent_user.save()
                        messages.success(request, "اطلاعات شما دریافت شد، نتیجه بررسی آن بزودی تعیین می‌شود.")
                        return HttpResponseRedirect(reverse('agent_profile_info_now'))
            else:
                if agent_user.complete_info == 'dnt':
                    form = AgentInfoCompletionForm()
                else:
                    form = AgentInfoEditForm()
            context['form'] = form

        except AgentCustomUserModel.DoesNotExist:
            user = CustomUserModel.objects.get(phone_number=phone_number)
            context['user'] = user
            print('CUNT')
    else:
        user = request.user
        context['user'] = user
        print('DICK')
    return render(request, 'agents/agent_profile_info_now.html', context)


