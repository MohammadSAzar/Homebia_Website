from django import forms
from .models import SaleFile, generate_unique_id
from django.utils import timezone
from django.utils.text import slugify


create_file_fields = ['province', 'city', 'district', 'price', 'room', 'area', 'year', 'document', 'level', 'parking', 'elevator',
                      'warehouse', 'document', 'title', 'description', 'cover', 'cover2', 'cover3', 'cover4',
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

    def save(self, commit=True):
        instance = super(SaleFileCreateForm, self).save(commit=False)

        if instance.pk is not None:
            old_status = SaleFile.objects.get(pk=instance.pk).status
            if old_status == 'pen' and instance.status == 'acc':
                instance.datetime_expired = timezone.now() + timezone.timedelta(days=60)

        if not instance.slug:
            instance.slug = slugify(instance.title)

        if commit:
            instance.save()

        return instance

