from django import forms
from django.utils.translation import gettext as _

from . import models
from .models import SaleFile, RentFile, Province, City, District, TradeSession
from . import checkers, choices


create_file_fields = ['province', 'city', 'district', 'price', 'room', 'area', 'age', 'document', 'level', 'parking', 'elevator',
                      'warehouse', 'title', 'description', 'cover', 'cover2', 'cover3', 'cover4', 'direction', 'file_levels',
                      'aparts_per_level', 'balcony', 'bench_stove', 'restoration', 'toilet', 'hot_water', 'cooling', 'heating',
                      'floor', 'provider_name', 'phone_number_for_contact', 'provider_national_code', 'owner_national_code',
                      'file_postal_code']


create_rent_file_fields = ['province', 'city', 'district', 'price_deposit', 'price_rent', 'convertable', 'room', 'area', 'age',
                           'document', 'level', 'parking', 'elevator','warehouse', 'title', 'description', 'cover', 'cover2',
                           'cover3', 'cover4', 'direction', 'file_levels', 'aparts_per_level', 'balcony', 'bench_stove', 'restoration',
                           'toilet', 'hot_water', 'cooling', 'heating', 'floor', 'provider_name', 'phone_number_for_contact',
                           'provider_national_code', 'owner_national_code', 'file_postal_code']


sale_required_fields = ['province', 'city', 'price', 'room', 'area', 'age', 'document', 'level', 'parking', 'elevator',
                        'warehouse', 'title', 'description', 'cover', 'provider_name', 'phone_number_for_contact',
                        'provider_national_code', 'owner_national_code', 'file_postal_code']


rent_required_fields = ['province', 'city', 'price_deposit', 'price_rent', 'convertable', 'room', 'area', 'age', 'document',
                        'level', 'parking', 'elevator', 'warehouse', 'title', 'description', 'cover', 'provider_name',
                        'phone_number_for_contact', 'provider_national_code', 'owner_national_code', 'file_postal_code']


class SaleFileCreateForm(forms.ModelForm):
    class Meta:
        model = SaleFile
        fields = create_file_fields
        widgets = {
            'province': forms.Select(attrs={'id': 'province'}),
            'city': forms.Select(attrs={'id': 'city'}),
            'district': forms.Select(attrs={'id': 'district'})
        }

    def __init__(self, *args, **kwargs):
        super(SaleFileCreateForm, self).__init__(*args, **kwargs)
        for field in sale_required_fields:
            self.fields[field].required = True

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
            self.add_error('area', 'متراژ فایل باید بین 20 تا 10000 متر باشد.')
        if phone_number_for_contact and not checkers.phone_checker(phone_number_for_contact):
            self.add_error('phone_number_for_contact', 'شماره تلفن همراه وارد شده معتبر نیست.')
        if file_postal_code and not checkers.postal_code_checker(file_postal_code):
            self.add_error('file_postal_code', 'کد پستی وارد شده معتبر نیست.')
        if provider_national_code and not checkers.national_code_checker(provider_national_code):
            self.add_error('provider_national_code', 'کد ملی وارد شده معتبر نیست.')
        if owner_national_code and not checkers.national_code_checker(owner_national_code):
            self.add_error('owner_national_code', 'کد ملی وارد شده معتبر نیست.')

        return cleaned_data


class SaleFileFilterForm(forms.Form):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), required=False, label=_('Province'))
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, label=_('City'))
    district = forms.ModelChoiceField(queryset=District.objects.all(), required=False, label=_('District'))
    min_price = forms.IntegerField(required=False, label=_('Min Price'))
    max_price = forms.IntegerField(required=False, label=_('Max Price'))
    min_area = forms.IntegerField(required=False, label=_('Min Area'))
    max_area = forms.IntegerField(required=False, label=_('Max Area'))
    min_room = forms.ChoiceField(choices=[('', '---------')] + choices.rooms, required=False, label=_('Min Room'))
    max_room = forms.ChoiceField(choices=[('', '---------')] + choices.rooms, required=False, label=_('Max Room'))
    min_age = forms.ChoiceField(choices=[('', '---------')] + choices.ages, required=False, label=_('Min Age'))
    max_age = forms.ChoiceField(choices=[('', '---------')] + choices.ages, required=False, label=_('Max Age'))
    min_level = forms.ChoiceField(choices=[('', '---------')] + choices.levels, required=False, label=_('Min Level'))
    max_level = forms.ChoiceField(choices=[('', '---------')] + choices.levels, required=False, label=_('Max Level'))
    document = forms.ChoiceField(choices=[('', '---------')] + choices.booleans, required=False, label=_('Document'))
    parking = forms.ChoiceField(choices=[('', '---------')] + choices.booleans, required=False, label=_('Parking'))
    elevator = forms.ChoiceField(choices=[('', '---------')] + choices.booleans, required=False, label=_('Elevator'))
    warehouse = forms.ChoiceField(choices=[('', '---------')] + choices.booleans, required=False, label=_('Warehouse'))

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        min_area = cleaned_data.get('min_area')
        max_area = cleaned_data.get('max_area')

        if min_price and not checkers.file_price_checker(min_price):
            self.add_error('min_price', 'قیمت فایل باید بین 1 تا 1000 میلیارد تومان باشد')

        if max_price and not checkers.file_price_checker(max_price):
            self.add_error('max_price', 'قیمت فایل باید بین 1 تا 1000 میلیارد تومان باشد')

        if min_area and not checkers.area_checker(min_area):
            self.add_error('min_area', 'متراژ فایل باید بین 20 تا 10000 متر باشد.')

        if max_area and not checkers.area_checker(max_area):
            self.add_error('max_area', 'متراژ فایل باید بین 20 تا 10000 متر باشد.')

        return cleaned_data


class RentFileCreateForm(forms.ModelForm):
    class Meta:
        model = RentFile
        fields = create_rent_file_fields
        widgets = {
            'province': forms.Select(attrs={'id': 'province'}),
            'city': forms.Select(attrs={'id': 'city'}),
            'district': forms.Select(attrs={'id': 'district'})
        }

    def __init__(self, *args, **kwargs):
        super(RentFileCreateForm, self).__init__(*args, **kwargs)
        for field in rent_required_fields:
            self.fields[field].required = True

    def clean(self):
        cleaned_data = super().clean()
        price_deposit = cleaned_data.get('price_deposit')
        price_rent = cleaned_data.get('price_rent')
        area = cleaned_data.get('area')
        phone_number_for_contact = cleaned_data.get('phone_number_for_contact')
        file_postal_code = cleaned_data.get('file_postal_code')
        provider_national_code = cleaned_data.get('provider_national_code')
        owner_national_code = cleaned_data.get('owner_national_code')
        description = cleaned_data.get('description')

        if price_deposit and not checkers.rent_file_deposit_price_checker(price_deposit):
            self.add_error('price_deposit', 'مبلغ ودیعه باید بین 0 تا 100 میلیارد تومان باشد')

        if price_rent and not checkers.rent_file_rent_price_checker(price_rent):
            self.add_error('price_rent', 'مبلغ اجاره باید بین 0 تا 1 میلیارد تومان باشد')

        if area and not checkers.area_checker(area):
            self.add_error('area', 'متراژ فایل باید بین 20 تا 10000 متر باشد.')

        if phone_number_for_contact and not checkers.phone_checker(phone_number_for_contact):
            self.add_error('phone_number_for_contact', 'شماره تلفن همراه وارد شده معتبر نیست.')

        if file_postal_code and not checkers.postal_code_checker(file_postal_code):
            self.add_error('file_postal_code', 'کد پستی وارد شده معتبر نیست.')

        if provider_national_code and not checkers.national_code_checker(provider_national_code):
            self.add_error('provider_national_code', 'کد ملی وارد شده معتبر نیست.')

        if owner_national_code and not checkers.national_code_checker(owner_national_code):
            self.add_error('owner_national_code', 'کد ملی وارد شده معتبر نیست.')

        if not description:
            self.add_error('description', 'این فیلد لازم است.')

        return cleaned_data


class RentFileFilterForm(forms.Form):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), required=False, label=_('Province'))
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, label=_('City'))
    district = forms.ModelChoiceField(queryset=District.objects.all(), required=False, label=_('District'))
    min_price_deposit = forms.IntegerField(required=False, label=_('Min Price Deposit'))
    max_price_deposit = forms.IntegerField(required=False, label=_('Max Price Deposit'))
    min_price_rent = forms.IntegerField(required=False, label=_('Min Price Rent'))
    max_price_rent = forms.IntegerField(required=False, label=_('Max Price Rent'))
    convertable = forms.ChoiceField(choices=[('', '---------')] + choices.beings, required=False, label=_('Convertable'))
    min_area = forms.IntegerField(required=False, label=_('Min Area'))
    max_area = forms.IntegerField(required=False, label=_('Max Area'))
    min_room = forms.ChoiceField(choices=[('', '---------')] + choices.rooms, required=False, label=_('Min Room'))
    max_room = forms.ChoiceField(choices=[('', '---------')] + choices.rooms, required=False, label=_('Max Room'))
    min_age = forms.ChoiceField(choices=[('', '---------')] + choices.ages, required=False, label=_('Min Age'))
    max_age = forms.ChoiceField(choices=[('', '---------')] + choices.ages, required=False, label=_('Max Age'))
    min_level = forms.ChoiceField(choices=[('', '---------')] + choices.levels, required=False, label=_('Min Level'))
    max_level = forms.ChoiceField(choices=[('', '---------')] + choices.levels, required=False, label=_('Max Level'))
    document = forms.ChoiceField(choices=[('', '---------')] + choices.booleans, required=False, label=_('Document'))
    parking = forms.ChoiceField(choices=[('', '---------')] + choices.booleans, required=False, label=_('Parking'))
    elevator = forms.ChoiceField(choices=[('', '---------')] + choices.booleans, required=False, label=_('Elevator'))
    warehouse = forms.ChoiceField(choices=[('', '---------')] + choices.booleans, required=False, label=_('Warehouse'))

    def clean(self):
        cleaned_data = super().clean()
        min_price_deposit = cleaned_data.get('min_price_deposit')
        max_price_deposit = cleaned_data.get('max_price_deposit')
        min_price_rent = cleaned_data.get('min_price_rent')
        max_price_rent = cleaned_data.get('max_price_rent')
        min_area = cleaned_data.get('min_area')
        max_area = cleaned_data.get('max_area')

        if min_price_deposit and not checkers.file_price_checker(min_price_deposit):
            self.add_error('min_price_deposit', 'مبلغ ودیعه باید بین 0 تا 100 میلیارد تومان باشد')

        if max_price_deposit and not checkers.file_price_checker(max_price_deposit):
            self.add_error('max_price_deposit', 'مبلغ ودیعه باید بین 0 تا 100 میلیارد تومان باشد')

        if min_price_rent and not checkers.file_price_checker(min_price_rent):
            self.add_error('min_price_rent', 'مبلغ اجاره باید بین 0 تا 1 میلیارد تومان باشد')

        if max_price_rent and not checkers.file_price_checker(max_price_rent):
            self.add_error('max_price_rent', 'مبلغ اجاره باید بین 0 تا 1 میلیارد تومان باشد')

        if min_area and not checkers.area_checker(min_area):
            self.add_error('min_area', 'متراژ فایل باید بین 20 تا 10000 متر باشد.')

        if max_area and not checkers.area_checker(max_area):
            self.add_error('max_area', 'متراژ فایل باید بین 20 تا 10000 متر باشد.')

        return cleaned_data


class TradeSessionForm(forms.ModelForm):
    class Meta:
        model = models.TradeSession
        fields = ['trade_type', 'city', 'ours', 'sale_file', 'sale_code', 'rent_file', 'rent_code', 'location', 'date',
                  'time', 'name_and_family', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        sale_code = cleaned_data.get('sale_code')
        rent_code = cleaned_data.get('rent_code')
        sale_codes = SaleFile.objects.values_list('code', flat=True)
        rent_codes = RentFile.objects.values_list('code', flat=True)

        if sale_code and sale_code not in sale_codes:
            self.add_error('sale_code', 'کد آگهی فروش وارد شده موجود نیست!')

        if rent_code and rent_code not in rent_codes:
            self.add_error('rent_code', 'کد آگهی اجاره وارد شده موجود نیست!')

        return cleaned_data


class SaleTradeSessionForm(forms.ModelForm):
    class Meta:
        model = models.TradeSession
        fields = ['city', 'sale_code', 'location', 'date', 'time', 'name_and_family', 'phone_number']


class RentTradeSessionForm(forms.ModelForm):
    class Meta:
        model = models.TradeSession
        fields = ['city', 'rent_code', 'location', 'date', 'time', 'name_and_family', 'phone_number']


