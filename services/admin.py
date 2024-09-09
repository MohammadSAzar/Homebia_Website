from django.contrib import admin

from .models import Counseling, Session, Visit


@admin.register(Counseling)
class CounselingAdmin(admin.ModelAdmin):
    list_display = ('counseling_type', 'date', 'time', 'name_and_family', 'phone_number', 'datetime_created',
                    'agent_status', 'status')
    ordering = ('-datetime_created', )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'customer_type', 'date', 'time', 'name_and_family', 'phone_number',
                    'datetime_created', 'agent_status', 'status')
    ordering = ('-datetime_created', )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'date', 'time', 'name_and_family', 'phone_number', 'datetime_created',
                    'agent_status', 'status')
    ordering = ('-datetime_created', )


