from django import forms
from django.utils import timezone
from django.utils.text import slugify

from .models import SaleFile, generate_unique_id
from . import checkers


create_file_fields = ['province', 'city', 'district', 'price', 'room', 'area', 'year', 'document', 'level', 'parking', 'elevator',
                      'warehouse', 'title', 'description', 'cover', 'cover2', 'cover3', 'cover4',
                      'direction', 'file_levels', 'aparts_per_level', 'balcony', 'bench_stove', 'restoration', 'toilet',
                      'hot_water', 'cooling', 'heating', 'floor', 'provider_name', 'phone_number_for_contact',
                      'provider_national_code', 'owner_national_code', 'file_postal_code']

class SaleFileCreateForm(forms.ModelForm):
    class Meta:
        model = SaleFile
        fields = create_file_fields
        widgets = {
            'province': forms.Select(attrs={'id': 'province'}),
            'city': forms.Select(attrs={'id': 'city'}),
            'district': forms.Select(attrs={'id': 'district'})
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        area = cleaned_data.get('area')
        phone_number_for_contact = cleaned_data.get('phone_number_for_contact')
        file_postal_code = cleaned_data.get('file_postal_code')
        provider_national_code = cleaned_data.get('provider_national_code')
        owner_national_code = cleaned_data.get('owner_national_code')

        if price and not checkers.file_price_checker(price):
            self.add_error('price', 'قیمت فایل باید بین 1 تا 1000 میلیارد تومان باشد')

        if area and not checkers.area_checker(area):
            self.add_error('area', 'متراژ فایل باید بین 1 تا 10000 متر باشد.')

        if phone_number_for_contact and not checkers.phone_checker(phone_number_for_contact):
            self.add_error('phone_number_for_contact', 'شماره تلفن همراه وارد شده معتبر نیست.')

        if file_postal_code and not checkers.postal_code_checker(file_postal_code):
            self.add_error('file_postal_code', 'کد پستی وارد شده معتبر نیست.')

        if provider_national_code and not checkers.national_code_checker(provider_national_code):
            self.add_error('provider_national_code', 'کد ملی وارد شده معتبر نیست.')

        if owner_national_code and not checkers.national_code_checker(owner_national_code):
            self.add_error('owner_national_code', 'کد ملی وارد شده معتبر نیست.')

        return cleaned_data


