from django.urls import path, re_path, include

from . import views


urlpatterns = [
    path('load_case_cities/', views.load_cities, name='load_case_cities'),
    path('load_case_districts/', views.load_districts, name='load_case_districts'),
    path('get_case_cities/', views.load_cities_list, name='load_case_cities_list'),
    path('get_case_districts/', views.load_districts_list, name='load_case_districts_list'),
    path('case/list', views.CaseListView.as_view(), name='case_list'),
    path('add/<int:case_id>/', views.add_to_cart_view, name='cart_add'),
    path('remove/<int:case_id>/', views.remove_from_cart_view, name='cart_remove'),
    path('cart/detail/', views.cart_detail_view, name='cart_detail'),
    path('cart/empty/', views.cart_empty_view, name='cart_empty'),
    path('clear/', views.cart_clear, name='cart_clear'),
    # path('order/create/', views.order_create_view, name='order_create'),
    re_path(r'case-detail/(?P<slug>[-\w]+)/(?P<unique_url_id>[-\w]+)/', views.CaseDetailView.as_view(), name='case_detail'),
]

