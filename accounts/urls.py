from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    path('verification/', views.verification_view, name='verification'),
    path('profile/', views.profile_info_now, name='profile_info_now'),
    path('info_auth/', views.profile_info_auth, name='profile_info_auth'),
    path('info_edit/', views.profile_info_edit, name='profile_info_edit'),
    path('your_services/', views.profile_your_services, name='profile_your_services'),
    path('your_trades/', views.profile_your_trades, name='profile_your_trades'),
    path('your_cases/', views.profile_your_cases, name='profile_your_cases'),
]

