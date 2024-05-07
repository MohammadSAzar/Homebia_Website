from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.utils.translation import gettext as _
from django.contrib import messages

from .models import Blog
from .forms import BlogCommentForm

class BlogListView(ListView):
    queryset = Blog.objects.select_related('blog_category').filter(status='pub')
    paginate_by = 6
    context_object_name = 'blogs'
    template_name = 'blog/blog_list.html'


# def blog_detail(request, slug):
#     # blog = get_object_or_404(Blog, slug=slug)
#     blog = Blog.objects.select_related('author').get(slug=slug)
#     context = {'blog': blog}
#     return render(request, 'blog/blog_detail.html', context)

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Blog.objects.select_related('blog_category').filter(slug=slug)

    # def get_context_data(self, **kwargs):
    #     context = super(BlogDetailView, self).get_context_data(**kwargs)
    #     context['blogs'] = Blog.objects.filter(status='pub').values('title', 'date_creation').order_by('-date_creation')[:5]
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(status='pub').values('title', 'date_creation').order_by('-date_creation')[:5]
        context['comments'] = self.object.comments.all()
        context['comment_form'] = BlogCommentForm()
        return context

# ******************* Blog category views ******************* #
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

