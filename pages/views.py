from django.shortcuts import render, redirect

from blog.models import Blog
from accounts.models import CustomUserModel
from agents.models import AgentCustomUserModel


def home_view(request):
    context = {}
    blogs = Blog.objects.select_related('blog_category').filter(status='pub').order_by('-date_creation')[:6]
    context['blogs'] = blogs
    user_now = request.user
    if isinstance(user_now, CustomUserModel):
        context['user'] = user_now
    else:
        phone_number = request.session.get('user_phone_number')
        if phone_number:
            agent_user = AgentCustomUserModel.objects.get(phone_number=phone_number)
            context['agent_user'] = agent_user
        context['user'] = user_now
    return render(request, 'pages/home.html', context)


def services_view(request):
    return render(request, 'pages/services.html')


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

