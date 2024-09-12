from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Counseling, Session, Visit
from agents.models import Task


@admin.register(Counseling)
class CounselingAdmin(admin.ModelAdmin):
    list_display = ('counseling_type', 'is_requested', 'task_link', 'date', 'time', 'name_and_family', 'phone_number',
                    'datetime_created', 'status')
    ordering = ('-datetime_created', )

    def is_requested(self, obj):
        counseling_task = Task.objects.filter(task_counseling=obj).first()
        if counseling_task:
            return counseling_task.is_requested
    is_requested.short_description = 'is_requested'

    def task_link(self, obj):
        task = Task.objects.filter(task_counseling=obj).first()
        if task:
            url = reverse("admin:agents_task_change", args=[task.id])
            return format_html('<a href="{}">View Task</a>', url)
    task_link.short_description = 'task_link'


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'is_requested', 'task_link', 'customer_type', 'date', 'time', 'name_and_family', 'phone_number',
                    'datetime_created', 'status')
    ordering = ('-datetime_created', )

    def is_requested(self, obj):
        session_task = Task.objects.filter(task_session=obj).first()
        if session_task:
            return session_task.is_requested
    is_requested.short_description = 'is_requested'

    def task_link(self, obj):
        task = Task.objects.filter(task_session=obj).first()
        if task:
            url = reverse("admin:agents_task_change", args=[task.id])
            return format_html('<a href="{}">View Task</a>', url)
    task_link.short_description = 'task_link'


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'is_requested', 'task_link', 'date', 'time', 'name_and_family', 'phone_number',
                    'datetime_created', 'status')
    ordering = ('-datetime_created', )

    def is_requested(self, obj):
        visit_task = Task.objects.filter(task_visit=obj).first()
        if visit_task:
            return visit_task.is_requested
    is_requested.short_description = 'is_requested'

    def task_link(self, obj):
        task = Task.objects.filter(task_visit=obj).first()
        if task:
            url = reverse("admin:agents_task_change", args=[task.id])
            return format_html('<a href="{}">View Task</a>', url)
    task_link.short_description = 'task_link'


