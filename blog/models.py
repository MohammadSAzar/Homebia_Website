from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as _
from tinymce.models import HTMLField
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField


class BlogCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Category title'))
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(BlogCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_category', args=[self.title])


class Blog(models.Model):
    STATUS_CHOICES = (('pub', 'Published'), ('drf', 'Draft'))
    cover = models.ImageField(upload_to='blogs/', verbose_name=_('Blog cover'))
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name='posts', verbose_name=_('Blog category'))
    title = models.CharField(max_length=200, verbose_name=_('Blog title'))
    body = HTMLField(verbose_name=_('Blog body'))
    date_creation = models.DateField(auto_now_add=True, verbose_name=_('Datetime of creation'))
    date_modification = models.DateField(auto_now=True, verbose_name=_('Datetime of modification'))
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True, allow_unicode=True)
    author = models.ForeignKey('accounts.CustomUserModel', on_delete=models.CASCADE, verbose_name=_('Blog author'))
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, verbose_name=_('Blog status'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Blog, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-date_creation',)

    def __str__(self):
        return self.title + '|' + str(self.author)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])


# class BlogComment(models.Model):
#     text = models.TextField()
#     date_time_creation = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
#     is_active = models.BooleanField(default=True)
#     recommend = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.text


