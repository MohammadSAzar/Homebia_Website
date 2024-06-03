from django.contrib import admin

from .models import Province, City, District, File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
	list_display = (
		'title', 'slug', 'status', 'province', 'city', 'district', 'provider_name', 'phone_number_for_contact', 'price',
		'room', 'area', 'year', 'document', 'level', 'parking', 'elevator', 'warehouse', 'cover', 'cover2', 'cover3', 'cover4',
		'unique_url_id', 'datetime_created',)
	ordering = ('-datetime_created',)
	prepopulated_fields = {'slug': ('title',)}


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
	list_display = ('name', 'province')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
	list_display = ('name', 'city')


