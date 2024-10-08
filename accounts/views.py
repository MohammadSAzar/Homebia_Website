from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView


from .models import CustomUserModel, Profile, Task
from .forms import RegistrationForm, AuthenticationForm, InfoEditForm, AgentRequestForm, TaskApplyForm
from .checkers import send_otp, get_random_otp, otp_time_checker

from services.models import Counseling, Session, Visit
from restates.models import TradeSession
from cases.models import Case, CaseOrder, CaseOrderItem


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
                return HttpResponseRedirect(reverse('verification'))
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
def profile_info_now_view(request):
    context = {}
    phone_number = request.session.get('user_phone_number')
    if phone_number:
        user = CustomUserModel.objects.get(phone_number=phone_number)
        context['user'] = user
    else:
        user = request.user
        context['user'] = user
    return render(request, 'accounts/profile_info_now.html', context)


def profile_info_auth_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            profile = form.save(commit=False)
            # profile.user = user
            profile.save()
            user.profile = profile
            form.save()
            user.is_verified = 'i'
            user.save()
            messages.success(request, "اطلاعات شما دریافت شد، نتیجه فرایند احراز هویت بزودی تعیین می‌شود.")
            return HttpResponseRedirect(reverse('profile_info_now'))
    else:
        print('cock')
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    print('piss')
    return render(request, 'accounts/profile_info_auth.html', context)


def profile_info_edit_view(request):
    if request.method == 'POST':
        form = InfoEditForm(request.POST)
        user = request.user
        profile = Profile.objects.get(user=user)
        if form.is_valid():
            form.save()
            profile.save()
            messages.success(request, "اطلاعات شما با موفقیت اصلاح شد.")
            return HttpResponseRedirect(reverse('profile_info_now'))
    else:
        form = InfoEditForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/profile_info_edit.html', context)


def profile_your_services_view(request):
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


def profile_your_trades_view(request):
    phone_number = request.session.get('user_phone_number')
    trades = TradeSession.objects.select_related('rent_file', 'sale_file').filter(phone_number=phone_number).all()
    context = {
        'trades': trades,
    }
    return render(request, 'accounts/profile_your_trades.html', context)


def profile_your_cases_view(request):
    phone_number = request.session.get('user_phone_number')
    case_orders = CaseOrder.objects.prefetch_related('item__case').filter(user__phone_number=phone_number).all()
    context = {
        'case_orders': case_orders,
    }
    return render(request, 'accounts/profile_your_cases.html', context)


# --------------------------------- Task ---------------------------------
class AgentTaskListView(ListView):
    model = Task
    template_name = 'accounts/agent_task_list.html'
    context_object_name = 'tasks'
    paginate_by = 6
    queryset = Task.objects.select_related('task_counseling').select_related('task_session').select_related('task_visit')\
        .select_related('task_trade_session').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone_number = self.request.session.get('user_phone_number')
        if phone_number:
            user = CustomUserModel.objects.get(phone_number=phone_number)
            context['user'] = user
        else:
            user = self.request.user
            context['user'] = user
        return context


class AgentTaskCounselingListView(ListView):
    model = Task
    template_name = 'accounts/agent_task_counseling_list.html'
    context_object_name = 'tasks'
    paginate_by = 6
    queryset = Task.objects.select_related('task_counseling').filter(type='cns').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone_number = self.request.session.get('user_phone_number')
        if phone_number:
            user = CustomUserModel.objects.get(phone_number=phone_number)
            context['user'] = user
        else:
            user = self.request.user
            context['user'] = user
        return context


class AgentTaskSessionListView(ListView):
    model = Task
    template_name = 'accounts/agent_task_session_list.html'
    context_object_name = 'tasks'
    paginate_by = 6
    queryset = Task.objects.select_related('task_session').filter(type='ses').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone_number = self.request.session.get('user_phone_number')
        if phone_number:
            user = CustomUserModel.objects.get(phone_number=phone_number)
            context['user'] = user
        else:
            user = self.request.user
            context['user'] = user
        return context


class AgentTaskVisitListView(ListView):
    model = Task
    template_name = 'accounts/agent_task_visit_list.html'
    context_object_name = 'tasks'
    paginate_by = 6
    queryset = Task.objects.select_related('task_visit').filter(type='vis').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone_number = self.request.session.get('user_phone_number')
        if phone_number:
            user = CustomUserModel.objects.get(phone_number=phone_number)
            context['user'] = user
        else:
            user = self.request.user
            context['user'] = user
        return context


class AgentTaskTradeSessionListView(ListView):
    model = Task
    template_name = 'accounts/agent_task_trade_session_list.html'
    context_object_name = 'tasks'
    paginate_by = 6
    queryset = Task.objects.select_related('task_trade_session').filter(type='tds').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone_number = self.request.session.get('user_phone_number')
        if phone_number:
            user = CustomUserModel.objects.get(phone_number=phone_number)
            context['user'] = user
        else:
            user = self.request.user
            context['user'] = user
        return context


def agent_task_detail_view(request, pk, unique_url_id):
    context = {}
    task = get_object_or_404(Task, unique_url_id=unique_url_id)
    context['task'] = task
    user = request.user
    context['user'] = user
    if request.method == 'POST':
        form = TaskApplyForm(request.POST)
        if form.is_valid():
            task.agent = user
            task.is_requested = 'pen'
            task.save()
            messages.success(request, "درخواست شما برای قبول این فرصت مشاوره دریافت شد. منتظر تماس از سوی ما یا مشتری باشید.")
            return redirect(reverse('agent_task_list'))
    else:
        form = TaskApplyForm()
    context['form'] = form

    return render(request, 'accounts/agent_task_detail.html', context=context)


def agent_request_view(request):
    if request.method == 'POST':
        form = AgentRequestForm(request.POST)
        user = request.user
        profile = Profile.objects.get(user=user)
        if form.is_valid():
            profile.experience = form.cleaned_data['experience']
            profile.introduction_way = form.cleaned_data['introduction_way']
            profile.course_tendency = form.cleaned_data['course_tendency']
            profile.save()
            user.is_agent = 'wt'
            user.save()
            messages.success(request, "اطلاعات شما دریافت شد، نتیجه درخواست همکاری شما بزودی تعیین می‌شود.")
            return HttpResponseRedirect(reverse('agent_request'))
    else:
        form = AgentRequestForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/agent_request.html', context)


def agent_activities_view(request):
    agent = request.user
    counseling_tasks = Task.objects.filter(agent=agent, task_counseling__isnull=False).all()
    session_tasks = Task.objects.filter(agent=agent, task_session__isnull=False).all()
    visit_tasks = Task.objects.filter(agent=agent, task_visit__isnull=False).all()
    trade_session_tasks = Task.objects.filter(agent=agent, task_trade_session__isnull=False).all()
    context = {
        'counseling_tasks': counseling_tasks,
        'session_tasks': session_tasks,
        'visit_tasks': visit_tasks,
        'trade_session_tasks': trade_session_tasks,
    }

    return render(request, 'accounts/agent_activities.html', context=context)


