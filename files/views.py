from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView
from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponseRedirect

from accounts.models import CustomUserModel
from accounts.forms import RegistrationForm
from accounts.helper import send_otp, get_random_otp, otp_time_checker

# from .models import File
# from .forms import FileCreateForm

def create_file_view(request):
	return render(request, 'files/file_create.html')

def file_registration_view(request):
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

