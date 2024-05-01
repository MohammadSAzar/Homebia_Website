from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.utils.translation import gettext as _
from django.contrib import messages

from .models import Blog

class BlogListView(ListView):
    queryset = Blog.objects.select_related('blog_category').filter(status='pub')
    paginate_by = 6
    context_object_name = 'blogs'
    template_name = 'blog/blog_list.html'


# class BlogDetailView(DetailView):
#     model = Blog
#     template_name = 'blog/blog_detail.html'
#     context_object_name = 'blog'

def blog_detail(request, slug):
    # blog = get_object_or_404(Blog, slug=slug)
    blog = Blog.objects.select_related('author').get(slug=slug)
    context = {'blog': blog}
    return render(request, 'blog/blog_detail.html', context)


def blog_category_homebia(request):
    blogs = Blog.objects.select_related('blog_category').filter(status='pub').filter(blog_category__title='هومبیا')
    context = {
        'blogs': blogs,
    }
    return render(request, 'blog/blog_category_homebia.html', context)

def blog_category_news(request):
    blogs = Blog.objects.select_related('blog_category').filter(status='pub').filter(blog_category__title='اخبار')
    context = {
        'blogs': blogs,
    }
    return render(request, 'blog/blog_category_news.html', context)

def blog_category_educational(request):
    blogs = Blog.objects.select_related('blog_category').filter(status='pub').filter(blog_category__title='آموزشی')
    context = {
        'blogs': blogs,
    }
    return render(request, 'blog/blog_category_educational.html', context)

def blog_category_analytical(request):
    blogs = Blog.objects.select_related('blog_category').filter(status='pub').filter(blog_category__title='تحلیلی')
    context = {
        'blogs': blogs,
    }
    return render(request, 'blog/blog_category_analytical.html', context)

# def blog_category(request, category):
#     blogs = Blog.objects.select_related('blog_category').filter(status='pub').filter(blog_category=category)
#     context = {
#         'blogs': blogs,
#     }
#     if category == 'هومبیا':
#         return render(request, 'blog/blog_category_homebia.html', context)
#     if category == 'آموزشی':
#         return render(request, 'blog/blog_category_educational.html', context)
#     if category == 'تحلیلی':
#         return render(request, 'blog/blog_category_analytical.html', context)
#     if category == 'اخبار':
#         return render(request, 'blog/blog_category_news.html', context)
