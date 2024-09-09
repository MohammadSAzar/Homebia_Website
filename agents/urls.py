from django.urls import path, re_path

from . import views

urlpatterns = [
    path('load_cities/', views.load_cities, name='load_cities'),
    path('get-cities/', views.load_cities_list, name='load_cities_list'),
    path('registration/', views.agent_registration_view, name='agent_registration'),
    path('verification/', views.agent_verification_view, name='agent_verification'),
    path('profile/', views.agent_profile_info_now, name='agent_profile_info_now'),
    path('task_list/', views.TaskListView.as_view(), name='task_list'),
    re_path(r'task_detail/(?P<unique_url_id>[-\w]+)/', views.TaskDetailView.as_view(), name='task_detail'),
    # path('info_auth/', views.profile_info_auth, name='profile_info_auth'),
    # path('info_edit/', views.profile_info_edit, name='profile_info_edit'),
    # path('your_services/', views.profile_your_services, name='profile_your_services'),
    # path('your_trades/', views.profile_your_trades, name='profile_your_trades'),
    # path('your_cases/', views.profile_your_cases, name='profile_your_cases'),
]

