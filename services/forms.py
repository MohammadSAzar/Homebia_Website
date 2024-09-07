from django import forms

from . import models


class CounselingForm(forms.ModelForm):
    class Meta:
        model = models.Counseling
        fields = ['city', 'district', 'counseling_type', 'date', 'time', 'name_and_family']

    def clean(self):
        cleaned_data = super().clean()
        counseling_type = self.cleaned_data['counseling_type']
        city = self.cleaned_data['city']
        district = self.cleaned_data['district']
        if counseling_type == 'ip':
            if not city:
                self.add_error('city', 'برای مشاوره حضوری، انتخاب شهر الزامی است.')
            if not district:
                self.add_error('district', 'برای مشاوره حضوری، تعیین محله الزامی است.')
        return cleaned_data


class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ['customer_type', 'city', 'district',  'date', 'time', 'name_and_family']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class VisitForm(forms.ModelForm):
    class Meta:
        model = models.Visit
        fields = ['city', 'district', 'date', 'time', 'name_and_family']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


