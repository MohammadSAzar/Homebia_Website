from django import forms
from .models import File

create_file_fields = ['province', 'city', 'district', 'price', 'room', 'area', 'year', 'document', 'level', 'parking', 'elevator',
                      'warehouse', 'document', 'title', 'description', 'cover', 'cover2', 'cover3', 'cover4',
                      'direction', 'file_levels', 'aparts_per_level', 'balcony', 'bench_stove', 'restoration', 'toilet',
                      'hot_water', 'cooling', 'heating', 'floor', 'provider_name', 'phone_number_for_contact',
                      'provider_national_code', 'owner_national_code', 'file_postal_code']

class FileCreateForm(forms.ModelForm):
    class Meta:
        model = File
        fields = create_file_fields
        widgets = {
            'province': forms.Select(attrs={'id': 'province'}),
            'city': forms.Select(attrs={'id': 'city'}),
            'district': forms.Select(attrs={'id': 'district'})
        }

# class FileCreateForm(forms.ModelForm):
#     class Meta:
#         model = File
#         fields = create_file_fields


