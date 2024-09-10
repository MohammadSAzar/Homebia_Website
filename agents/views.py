from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView


from .models import AgentCustomUserModel, AgentProfile, Task, Province, City
from accounts.models import CustomUserModel
from .forms import AgentRegistrationForm, AgentInfoCompletionForm, AgentInfoEditForm, AgentTaskApplyForm
from accounts.checkers import send_otp, get_random_otp, otp_time_checker_agent


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
                if user.otp_code is not None and otp_time_checker_agent(user.phone_number):
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
            if not otp_time_checker_agent(user.phone_number) or user.otp_code != int(request.POST.get('otp')):
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
    else:
        user = request.user
        context['user'] = user
    return render(request, 'agents/agent_profile_info_now.html', context)


# --------------------------------- tasks ---------------------------------
class TaskListView(ListView):
    model = Task
    template_name = 'agents/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20
    # queryset = Task.objects.select_related('task_counseling').select_related('task_session').select_related('task_visit').select_related('task_trade_session').all()
    queryset = Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone_number = self.request.session.get('user_phone_number')
        if phone_number:
            try:
                agent_user = AgentCustomUserModel.objects.get(phone_number=phone_number)
                context['agent_user'] = agent_user
            except AgentCustomUserModel.DoesNotExist:
                user = CustomUserModel.objects.get(phone_number=phone_number)
                context['user'] = user
        else:
            user = self.request.user
            context['user'] = user
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'agents/task_detail.html'
    context_object_name = 'task'

    # def post(self, request, *args, **kwargs):
    #     task_code = self.request.GET.get('code', '')
    #     task = get_object_or_404(Task, code=task_code)
    #     task.agent = self.request.agent_user


def task_detail(request, pk, unique_url_id):
    context = {}
    task = get_object_or_404(Task, unique_url_id=unique_url_id)
    context['task'] = task
    phone_number = request.user.phone_number
    if phone_number:
        try:
            agent_user = AgentCustomUserModel.objects.get(phone_number=phone_number)
            context['agent_user'] = agent_user
            if request.method == 'POST':
                form = AgentTaskApplyForm(request.POST)
                if form.is_valid():
                    task.agent = agent_user
                    task.is_requested = 'pen'
                    task.save()
                    return redirect(reverse('task_list'))
                else:
                    print(form.errors)
            else:
                form = AgentTaskApplyForm()
            context['form'] = form

        except AgentCustomUserModel.DoesNotExist:
            user = CustomUserModel.objects.get(phone_number=phone_number)
            context['user'] = user
    # else:
    #     user = request.user
    #     context['user'] = user

    return render(request, 'agents/task_detail.html', context=context)





