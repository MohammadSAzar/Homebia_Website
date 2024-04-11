from django import forms
from django.db import models
from jalali_date.fields import JalaliDateTimeField, JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from . import models

# class CounselingForm(forms.ModelForm):
#     class Meta:
#         model = models.Counseling
#         fields = ['customer_type', 'counseling_type', 'date', 'time', 'name_and_family', 'phone_number']
#         # widgets = {
#         #     'address': forms.Textarea(attrs={'rows': 5, 'placeholder': 'آدرس خود را وارد کنید...'}),
#         #     'notes': forms.Textarea(attrs={'rows': 5, 'placeholder': 'توضیحات خود را وارد کنید...'}),
#         # }

