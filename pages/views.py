from django.shortcuts import render, redirect
from django.db.models import Q

from blog.models import Blog
from accounts.models import CustomUserModel
from accounts.models import Task


def home_view(request):
    context = {}
    blogs = Blog.objects.select_related('blog_category').filter(status='pub').order_by('-date_creation')[:6]
    tasks = Task.objects.select_related('task_counseling').select_related('task_session').select_related('task_visit')\
                .select_related('task_trade_session').filter(Q(is_requested='fre') | Q(is_requested='pen'))\
                .order_by('-datetime_created')[:6]
    context['blogs'] = blogs
    context['tasks'] = tasks
    user_now = request.user
    if isinstance(user_now, CustomUserModel):
        context['user'] = user_now
    else:
        context['user'] = user_now

    return render(request, 'pages/home.html', context)


def four_o_four_view(request):
    return render(request, 'pages/404.html')


def contact_view(request):
    return render(request, 'pages/contact.html')


def about_view(request):
    return render(request, 'pages/about.html')


def rules_view(request):
    return render(request, 'pages/rules.html')


def faq_view(request):
    return render(request, 'pages/faq.html')

