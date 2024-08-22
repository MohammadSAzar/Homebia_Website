from django.shortcuts import render
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import AgentCustomUserModel, AgentProfile
from .forms import AgentRegistrationForm, AgentInfoCompletionForm
from .checkers import send_otp, get_random_otp, otp_time_checker


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
				return HttpResponseRedirect(reverse('agent_registration'))
			user.is_active = True
			user.save()
			login(request, user)
			return HttpResponseRedirect(reverse('agent_completion'))
		context = {
			'phone_number': phone_number,
		}
		return render(request, 'agents/agent_verification.html', context)
	except AgentCustomUserModel.DoesNotExist:
		return HttpResponseRedirect(reverse('agent_registration'))


def agent_completion_view(request):
	if request.method == 'POST':
		form = AgentInfoCompletionForm(request.POST)
		agent_user = request.user
		if form.is_valid():
			agent_profile = form.save(commit=False)
			agent_profile.user = agent_user
			agent_profile.save()
			form.save()
			agent_user.complete_info = 'ipr'
			agent_user.save()
			messages.success(request, "اطلاعات شما دریافت شد، نتیجه بررسی اطلاعات شما بزودی تعیین می‌شود.")
			return HttpResponseRedirect(reverse('agent_profile_info_now'))
	else:
		print('cock')
		form = AgentInfoCompletionForm()
	context = {
		'form': form,
	}
	print('piss')
	return render(request, 'agents/agent_completion.html', context)


def agent_profile_info_now(request):
	return render(request, 'agents/agent_profile_info_now.html')


