from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import CustomUserModel, Profile
from .forms import RegistrationForm, AuthenticationForm, IntoEditForm
from .checkers import send_otp, get_random_otp, otp_time_checker

from services.models import Counseling, Session, Visit
from restates.models import SaleFile, RentFile, TradeSession


def registration_view(request):
	form = RegistrationForm
	if request.method == 'POST':
		try:
			if 'phone_number' in request.POST:
				phone_number = request.POST.get('phone_number')
				user = CustomUserModel.objects.get(phone_number=phone_number)
				if user.otp_code is not None and otp_time_checker(user.phone_number):
					request.session['user_phone_number'] = user.phone_number
					return HttpResponseRedirect(reverse('verification'))
				otp = get_random_otp()
				send_otp(phone_number, otp)
				user.otp_code = otp
				user.save()
				request.session['user_phone_number'] = user.phone_number
				return HttpResponseRedirect(reverse('verification'))
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
				return HttpResponseRedirect(reverse('verification'))
	context = {
		'form': form,
	}
	return render(request, 'accounts/registration.html', context)


def verification_view(request):
	try:
		phone_number = request.session.get('user_phone_number')
		user = CustomUserModel.objects.get(phone_number=phone_number)
		if request.method == 'POST':
			if not otp_time_checker(user.phone_number) or user.otp_code != int(request.POST.get('otp')):
				return HttpResponseRedirect(reverse('registration'))
			user.is_active = True
			user.save()
			login(request, user)
			return HttpResponseRedirect(reverse('profile_info_now'))
		context = {
			'phone_number': phone_number,
		}
		return render(request, 'accounts/verification.html', context)
	except CustomUserModel.DoesNotExist:
		return HttpResponseRedirect(reverse('registration'))


# --------------------------------- Profile ---------------------------------
def profile_info_now(request):
	return render(request, 'accounts/profile_info_now.html')


def profile_info_auth(request):
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		user = request.user
		if form.is_valid():
			form.save()
			user.is_verified = 'i'
			user.save()
			return HttpResponseRedirect(reverse('profile_info_now'))
	else:
		form = AuthenticationForm()
	context = {
		'form': form,
	}
	return render(request, 'accounts/profile_info_auth.html', context)


def profile_info_edit(request):
	if request.method == 'POST':
		form = IntoEditForm(request.POST)
		user = request.user
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('profile_info_now'))
	else:
		form = IntoEditForm()
	context = {
		'form': form,
	}
	return render(request, 'accounts/profile_info_edit.html', context)


def profile_your_services(request):
	phone_number = request.session.get('user_phone_number')
	counselings = Counseling.objects.filter(phone_number=phone_number).all()
	sessions = Session.objects.filter(phone_number=phone_number).all()
	visits = Visit.objects.filter(phone_number=phone_number).all()
	context = {
		'counselings': counselings,
		'sessions': sessions,
		'visits': visits,
	}
	return render(request, 'accounts/profile_your_services.html', context)


def profile_your_trades(request):
	phone_number = request.session.get('user_phone_number')
	trades = TradeSession.objects.filter(phone_number=phone_number).all()
	context = {
		'trades': trades,
	}
	return render(request, 'accounts/profile_your_trades.html', context)



