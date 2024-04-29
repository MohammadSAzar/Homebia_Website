from django.urls import path, re_path, include

from . import views


urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    re_path(r'^blog/(?P<slug>[-\w]+)/', views.blog_detail_view, name='blog_detail'),
    re_path(r'^blog/(?P<slug>[-\w]+)/', views.blog_detail_view, name='category_blogs'),
]

