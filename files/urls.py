from django.urls import path

from . import views

urlpatterns = [
	path('file/create/', views.create_file_view, name='file_create'),
	# path('file/registration', views.file_registration_view, name='file_registration'),
	# path('file/verification', views.file_verification_view, name='file_verification'),
	# path('<slug:slug>/<str:unique_id>/', RealEstateFileDetailView.as_view(), name='file_detail'),
]
