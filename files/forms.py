from django import forms
from .models import File

class FileCreateForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['province', 'city', 'district', 'price', 'room', 'area', 'year', 'document', 'level', 'parking', 'elevator',
                  'warehouse', 'document', 'title', 'description',  # group1
                  'cover', 'cover2', 'cover3', 'cover4',  # group2
                  'direction', 'file_levels', 'aparts_per_level', 'balcony', 'bench_stove', 'restoration', 'toilet', 'hot_water',
                  'cooling', 'heating', 'floor',  # group3
                  'provider_name', 'phone_number_for_contact', 'provider_national_code', 'owner_national_code', 'file_postal_code'  # group4
                  ]


