from django import forms
from django.utils.translation import gettext as _

from .models import CaseOrder, Province, City, District
from . import checkers


class CaseFilterForm(forms.Form):
    CHOICES = [
        ('has', _('Has')),
        ('hasnt', _('Has not')),
    ]
    province = forms.ModelChoiceField(queryset=Province.objects.all(), required=False, label=_('Province'))
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, label=_('City'))
    district = forms.ModelChoiceField(queryset=District.objects.all(), required=False, label=_('District'))
    min_metric_price = forms.IntegerField(required=False, label=_('Min Metric Price'))
    max_metric_price = forms.IntegerField(required=False, label=_('Max Metric Price'))
    buy_assurance = forms.ChoiceField(choices=[('', '---------')] + CHOICES, required=False, label=_('Buy Assurance'))
    guaranteed_gain = forms.ChoiceField(choices=[('', '---------')] + CHOICES, required=False, label=_('Guaranteed Gain'))

    def clean(self):
        cleaned_data = super().clean()
        min_metric_price = cleaned_data.get('min_metric_price')
        max_metric_price = cleaned_data.get('max_metric_price')

        if min_metric_price and not checkers.case_metric_price_checker(min_metric_price):
            self.add_error('min_metric_price', 'قیمت هر متر باید بین 10 میلیون تا 1 میلیارد تومان باشد')

        if max_metric_price and not checkers.case_metric_price_checker(max_metric_price):
            self.add_error('max_metric_price', 'قیمت هر متر باید بین 10 میلیون تا 1 میلیارد تومان باشد')

        return cleaned_data


class AddToCartForm(forms.Form):
    CHOICES = [(i, str(i)) for i in range(1, 100)]
    meter = forms.TypedChoiceField(choices=CHOICES, coerce=int)
    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    class Meta:
        model = CaseOrder
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 5, 'placeholder': 'توضیحات خود را وارد کنید...'}),
        }
