from django.shortcuts import render, redirect


def home_view(request):
    return render(request, 'pages/home_new.html')


def services_view(request):
    return render(request, 'pages/services.html')

