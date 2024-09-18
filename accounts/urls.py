from django.urls import path, re_path

from . import views

urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    path('verification/', views.verification_view, name='verification'),
    path('profile/', views.profile_info_now_view, name='profile_info_now'),
    path('info_auth/', views.profile_info_auth_view, name='profile_info_auth'),
    path('info_edit/', views.profile_info_edit_view, name='profile_info_edit'),
    path('your_services/', views.profile_your_services_view, name='profile_your_services'),
    path('your_trades/', views.profile_your_trades_view, name='profile_your_trades'),
    path('your_cases/', views.profile_your_cases_view, name='profile_your_cases'),
    path('agent_request/', views.agent_request_view, name='agent_request'),
    path('agent_activities/', views.agent_activities_view, name='agent_activities'),
    path('agent_task_list/', views.AgentTaskListView.as_view(), name='agent_task_list'),
    re_path(r'task_detail/(?P<pk>[-\w]+)/(?P<unique_url_id>[-\w]+)/', views.agent_task_detail_view, name='agent_task_detail'),
]

