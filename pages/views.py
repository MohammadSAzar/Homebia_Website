from django.shortcuts import render, redirect

from blog.models import Blog


def home_view(request):
    blogs = Blog.objects.select_related('blog_category').filter(status='pub').order_by('-date_creation')[:6]
    context = {
        'blogs': blogs
    }
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

