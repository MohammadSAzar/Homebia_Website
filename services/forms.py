from django import forms
from . import models

class CounselingForm(forms.ModelForm):
    class Meta:
        model = models.Counseling
        fields = ['counseling_type', 'date', 'time', 'name_and_family']

class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ['customer_type', 'city', 'date', 'time', 'name_and_family']

class VisitForm(forms.ModelForm):
    class Meta:
        model = models.Visit
        fields = ['city', 'date', 'time', 'name_and_family']
