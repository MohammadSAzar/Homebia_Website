from django.urls import path, re_path, include

from . import views


urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    re_path(r'^blog/(?P<slug>[-\w]+)/', views.blog_detail, name='blog_detail'),
    path('category/homebia/', views.blog_category_homebia, name='category_homebia'),
    path('category/educational/', views.blog_category_educational, name='category_educational'),
    path('category/analytical/', views.blog_category_analytical, name='category_analytical'),
    path('category/news/', views.blog_category_news, name='category_news'),
]

