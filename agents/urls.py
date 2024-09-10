from django.urls import path, re_path

from . import views

urlpatterns = [
    path('load_cities/', views.load_cities, name='load_cities'),
    path('get-cities/', views.load_cities_list, name='load_cities_list'),
    path('registration/', views.agent_registration_view, name='agent_registration'),
    path('verification/', views.agent_verification_view, name='agent_verification'),
    path('profile/', views.agent_profile_info_now, name='agent_profile_info_now'),
    path('task_list/', views.TaskListView.as_view(), name='task_list'),
    re_path(r'task_detail/(?P<pk>[-\w]+)/(?P<unique_url_id>[-\w]+)/', views.task_detail, name='task_detail'),
]

