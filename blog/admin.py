from django.contrib import admin
# from jalali_date.admin import ModelAdminJalaliMixin
from .models import Blog, BlogCategory

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

