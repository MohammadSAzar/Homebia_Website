from django.urls import path, re_path
from . import views

urlpatterns = [
	path('sale_file_create/', views.SaleFileCreateView.as_view(), name='sale_file_create'),
	path('rent_file_create/', views.RentFileCreateView.as_view(), name='rent_file_create'),
	path('load_cities/', views.load_cities, name='load_cities'),
	path('load_districts/', views.load_districts, name='load_districts'),
	path('get-cities/', views.load_cities_list, name='load_cities_list'),
	path('get-districts/', views.load_districts_list, name='load_districts_list'),
	path('files/sale/', views.SaleFileListView.as_view(), name='sale_file_list'),
	re_path(r'sale-file/(?P<slug>[-\w]+)/(?P<unique_url_id>[-\w]+)/', views.SaleFileDetailView.as_view(), name='sale_file_detail'),
	path('files/rent/', views.RentFileListView.as_view(), name='rent_file_list'),
	re_path(r'rent-file/(?P<slug>[-\w]+)/(?P<unique_url_id>[-\w]+)/', views.RentFileDetailView.as_view(), name='rent_file_detail'),
]
