from django.contrib import admin

from .models import Province, City, District, SaleFile


@admin.register(SaleFile)
class SaleFileAdmin(admin.ModelAdmin):
	list_display = (
		'title', 'slug', 'status', 'province', 'city', 'district', 'provider_name', 'phone_number_for_contact', 'price',
		'room', 'area', 'year', 'document', 'level', 'parking', 'elevator', 'warehouse', 'cover', 'cover2', 'cover3', 'cover4',
		'unique_url_id', 'datetime_created', 'datetime_expired')
	ordering = ('-datetime_created',)
	prepopulated_fields = {'slug': ('title',)}
	list_filter = ('status', 'province', 'city')
	readonly_fields = ('unique_url_id', 'datetime_created', 'datetime_expired')


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
	list_display = ('name', 'province')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
	list_display = ('name', 'city')


