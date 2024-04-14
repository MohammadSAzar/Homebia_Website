from django import forms
from . import models

class RegistrationForm(forms.ModelForm):
	class Meta:
		model = models.CustomUserModel
		fields = ['phone_number']


class AuthenticationForm(forms.ModelForm):
	class Meta:
		model = models.Profile
		fields = ['f_name', 'l_name', 'sex', 'national_code', 'country', 'province', 'city', 'address', 'postal_code', 'national_card', 'auth_picture']


class IntoEditForm(forms.ModelForm):
	class Meta:
		model = models.Profile
		fields = ['f_name', 'l_name', 'province', 'city', 'address', 'postal_code']
