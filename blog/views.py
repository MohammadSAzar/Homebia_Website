from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404, render, HttpResponse, reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.contrib import messages

from .models import Blog, Comment, Reply
from .forms import CommentForm, ReplyForm

class BlogListView(ListView):
    queryset = Blog.objects.select_related('blog_category').filter(status='pub')
    paginate_by = 6
    context_object_name = 'blogs'
    template_name = 'blog/blog_list.html'


class BlogDetailView(DetailView):
    template_name = 'blog/blog_detail.html'
    model = Blog

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(blog=self.get_object())
        replies = Reply.objects.filter(blog=self.get_object())
        number_of_comments_and_replies = comments.count() + replies.count()
        data['comments'] = comments
        data['replies'] = replies
        data['number_of_comments_and_replies'] = number_of_comments_and_replies
        data['comment_form'] = CommentForm()
        data['reply_form'] = ReplyForm()
        return data

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            if 'reply_name' in self.request.POST:
                reply_form = ReplyForm(self.request.POST)
                print('PUSSSSSSSSSSSSSSSSSS')
                if reply_form.is_valid():
                    reply_name = reply_form.cleaned_data['reply_name']
                    body = reply_form.cleaned_data['body']

                    if reply_form.cleaned_data['parent_comment'] is not None:
                        parent_comment = reply_form.cleaned_data['parent_comment']
                        print('GOH')
                        parent_reply = None
                    else:
                        parent_comment = None
                        print('AN')
                        parent_reply = reply_form.cleaned_data['parent_reply']

                    new_reply = Reply(reply_name=reply_name, body=body, blog=self.get_object(), parent_comment=parent_comment, parent_reply=parent_reply)
                    new_reply.save()
            else:
                comment_form = CommentForm(self.request.POST)
                print('ASSSSSSSSSSSSSSSS')
                if comment_form.is_valid():
                    name = comment_form.cleaned_data['name']
                    body = comment_form.cleaned_data['body']
                    new_comment = Comment(name=name, body=body, blog=self.get_object())
                    new_comment.save()

            # return reverse(self.object.get_absolute_url())
            return HttpResponseRedirect(reverse('blog_list'))


# class BlogDetailView(FormMixin, DetailView):
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
#         context['comment_form'] = self.get_form()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         comment = form.save(commit=False)
#         comment.blog = self.object
#         comment.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()


# ************************************** Blog category views ************************************** #
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

