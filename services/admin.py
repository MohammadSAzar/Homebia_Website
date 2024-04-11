from django.contrib import admin

from .models import Counseling, Session, Visit

@admin.register(Counseling)
class CounselingAdmin(admin.ModelAdmin):
    list_display = ('counseling_type', 'customer_type', 'date', 'time', 'name_and_family', 'phone_number', 'datetime_created', 'status')
    ordering = ('-datetime_created', )
    # inlines = [
    #     ReviewInProductInline,
    # ]

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('city', 'customer_type', 'date', 'time', 'name_and_family', 'phone_number', 'datetime_created', 'status')
    ordering = ('-datetime_created', )

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('city', 'date', 'time', 'name_and_family', 'phone_number', 'datetime_created', 'status')
    ordering = ('-datetime_created', )


