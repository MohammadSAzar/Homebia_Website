from django.contrib import admin
# from jalali_date.admin import ModelAdminJalaliMixin
from .models import Blog, BlogCategory, BlogComment

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [
    #     ReviewInProductInline,
    # ]

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'blog_category', 'date_creation', 'date_modification')
    ordering = ('-date_creation', )
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [
    #     ReviewInProductInline,
    # ]

@admin.register(BlogComment)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog', 'name', 'body', 'is_active', 'date_time_creation')
    ordering = ('-date_time_creation',)

