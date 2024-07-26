from django import forms
from .models import CaseOrder


class AddToCart(forms.Form):
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
