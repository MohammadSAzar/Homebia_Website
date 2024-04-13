from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    path('verification/', views.verification_view, name='verification'),
    path('profile/info_now/', views.profile_info_now, name='profile_info_now'),
    path('profile/info_auth/', views.profile_info_auth, name='profile_info_auth'),
    path('profile/your_services/', views.profile_your_services, name='profile_your_services'),
    path('profile/your_cases/', views.profile_your_cases, name='profile_your_cases'),
    path('profile/your_files/', views.profile_your_files, name='profile_your_files'),
]

