from django.urls import path

from . import views

urlpatterns = [
    path('agent_registration/', views.agent_registration_view, name='agent_registration'),
    path('agent_verification/', views.agent_verification_view, name='agent_verification'),
    path('agent_profile/', views.agent_profile_info_now, name='agent_profile_info_now'),
    # path('info_auth/', views.profile_info_auth, name='profile_info_auth'),
    # path('info_edit/', views.profile_info_edit, name='profile_info_edit'),
    # path('your_services/', views.profile_your_services, name='profile_your_services'),
    # path('your_trades/', views.profile_your_trades, name='profile_your_trades'),
    # path('your_cases/', views.profile_your_cases, name='profile_your_cases'),
]

