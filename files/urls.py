from django.urls import path
from .views import load_cities, load_districts, real_estate_create

urlpatterns = [
	path('file/create/', real_estate_create, name='file_create'),
	path('load_cities/', load_cities, name='load_cities'),
	path('load_districts/', load_districts, name='load_districts'),
	# path('file/registration', views.file_registration_view, name='file_registration'),
	# path('file/verification', views.file_verification_view, name='file_verification'),
	# path('<slug:slug>/<str:unique_id>/', RealEstateFileDetailView.as_view(), name='file_detail'),
]
