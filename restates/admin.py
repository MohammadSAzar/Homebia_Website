from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Province, City, District, SaleFile, RentFile, TradeSession
from accounts.models import Task


@admin.register(SaleFile)
class SaleFileAdmin(admin.ModelAdmin):
	list_display = (
		'title', 'code', 'status', 'province', 'city', 'district', 'provider_name', 'phone_number_for_contact', 'price',
		'room', 'area', 'age', 'document', 'level', 'parking', 'elevator', 'warehouse', 'cover', 'cover2', 'cover3',
		'cover4',
		'unique_url_id', 'datetime_created', 'datetime_expired')
	ordering = ('-datetime_created',)
	prepopulated_fields = {'slug': ('title',)}
	list_filter = ('status', 'province', 'city')
	readonly_fields = ('unique_url_id', 'datetime_created', 'datetime_expired',)


@admin.register(RentFile)
class RentFileAdmin(admin.ModelAdmin):
	list_display = (
		'title', 'code', 'status', 'province', 'city', 'district', 'provider_name', 'phone_number_for_contact',
		'price_deposit',
		'price_rent', 'room', 'area', 'age', 'document', 'level', 'parking', 'elevator', 'warehouse', 'cover', 'cover2',
		'cover3', 'cover4', 'unique_url_id', 'datetime_created', 'datetime_expired')
	ordering = ('-datetime_created',)
	prepopulated_fields = {'slug': ('title',)}
	list_filter = ('status', 'province', 'city')
	readonly_fields = ('unique_url_id', 'datetime_created', 'datetime_expired',)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
	list_display = ('name', 'province')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
	list_display = ('name', 'city')


@admin.register(TradeSession)
class TradeSessionAdmin(admin.ModelAdmin):
	list_display = (
		'city', 'district', 'is_requested', 'task_link', 'trade_type', 'ours', 'sale_file', 'sale_code',
		'rent_file', 'rent_code', 'is_success', 'is_followed', 'is_paid', 'status', 'datetime_created', 'location',
		'date', 'time', 'name_and_family', 'phone_number')
	ordering = ('-datetime_created',)

	def is_requested(self, obj):
		trade_session_task = Task.objects.filter(task_trade_session=obj).first()
		if trade_session_task:
			return trade_session_task.is_requested
	is_requested.short_description = 'is_requested'

	def task_link(self, obj):
		task = Task.objects.filter(task_trade_session=obj).first()
		if task:
			url = reverse("admin:accounts_task_change", args=[task.id])
			return format_html('<a href="{}">View Task</a>', url)
	task_link.short_description = 'task_link'


