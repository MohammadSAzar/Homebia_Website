from django import forms
from . import models


class CounselingForm(forms.ModelForm):
    class Meta:
        model = models.Counseling
        fields = ['counseling_type', 'date', 'time', 'name_and_family']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ['customer_type', 'city', 'date', 'time', 'name_and_family']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class VisitForm(forms.ModelForm):
    class Meta:
        model = models.Visit
        fields = ['city', 'date', 'time', 'name_and_family']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


