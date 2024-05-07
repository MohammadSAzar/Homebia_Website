from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
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


class BlogDetailView(FormMixin, DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    form_class = BlogCommentForm

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Blog.objects.select_related('blog_category').filter(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(status='pub').values('title', 'date_creation').order_by('-date_creation')[:5]
        context['comments'] = self.object.comments.all()
        context['comment_form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.blog = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


# class BlogDetailView(DetailView):
#     model = Blog
#     template_name = 'blog/blog_detail.html'
#     context_object_name = 'blog'
#
#     def get_queryset(self):
#         slug = self.kwargs['slug']
#         return Blog.objects.select_related('blog_category').filter(slug=slug)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['blogs'] = Blog.objects.filter(status='pub').values('title', 'date_creation').order_by('-date_creation')[:5]
#         context['comments'] = self.object.comments.all()
#         context['comment_form'] = BlogCommentForm()
#         return context

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

