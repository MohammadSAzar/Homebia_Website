from django.urls import path

from . import views

urlpatterns = [
    path('counseling/', views.CounselingCreateView.as_view(), name='counseling'),
    path('counseling_detail/<int:id>/', views.CounselingDetailView.as_view(), name='counseling_detail'),
    path('session/', views.SessionCreateView.as_view(), name='session'),
    path('session_detail/<int:id>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('visit/', views.VisitCreateView.as_view(), name='visit'),
    path('visit_detail/<int:id>/', views.VisitDetailView.as_view(), name='visit_detail'),
]


