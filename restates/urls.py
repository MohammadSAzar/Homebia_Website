from django.urls import path, re_path
from . import views

urlpatterns = [
	path('file_create/', views.SaleFileCreateView.as_view(), name='file_create'),
	path('load_cities/', views.load_cities, name='load_cities'),
	path('load_districts/', views.load_districts, name='load_districts'),
	path('get-cities/', views.load_cities_list, name='load_cities_list'),
	path('get-districts/', views.load_districts_list, name='load_districts_list'),
	path('files/sale/', views.SaleFileListView.as_view(), name='file_list'),
	# re_path(r'(?P<slug>[-\w]+)/(?P<unique_url_id>[-\w]+)/', views.SaleFileDetailView.as_view(), name='file_detail'),
	re_path(r'/file/(?P<slug>[-\w]+)/(?P<unique_url_id>[-\w]+)/', views.SaleFileDetailView.as_view(), name='file_detail'),
]
