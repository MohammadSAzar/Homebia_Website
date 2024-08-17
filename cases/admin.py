from django.contrib import admin

from .models import Case, CaseOrder, CaseOrderItem, Province, City, District


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
	list_display = ('name', 'province')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
	list_display = ('name', 'city')


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
	list_display = (
		'title', 'maker', 'province', 'city', 'district', 'capacity', 'metric_price', 'buy_assurance',
		'guaranteed_gain', 'guaranteed_gain_percent', 'end_time', 'cover', 'cover2', 'cover2', 'cover4',
		'status', 'unique_url_id', 'code', 'datetime_created'
	)
	ordering = ('-datetime_created',)
	prepopulated_fields = {'slug': ('title',)}


@admin.register(CaseOrder)
class CaseOrderAdmin(admin.ModelAdmin):
	list_display = ('code', 'user', 'status', 'is_paid', 'datetime_created', 'datetime_modified')
	ordering = ('-datetime_created',)


@admin.register(CaseOrderItem)
class CaseOrderItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'order', 'case', 'meter')

