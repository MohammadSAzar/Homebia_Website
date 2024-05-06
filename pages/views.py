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

