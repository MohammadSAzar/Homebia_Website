from django.urls import path, re_path
from . import views

urlpatterns = [
	path('file/create/', views.real_estate_create, name='file_create'),
	path('load_cities/', views.load_cities, name='load_cities'),
	path('load_districts/', views.load_districts, name='load_districts'),
	path('files/sale/', views.SaleFileListView.as_view(), name='file_list'),
	# path('<slug:slug>/<str:unique_url_id>/', views.SaleFileDetailView.as_view(), name='file_detail'),
	re_path(r'(?P<slug>[-\w]+)/(?P<unique_url_id>[-\w]+)/', views.SaleFileDetailView.as_view(), name='file_detail'),
]
