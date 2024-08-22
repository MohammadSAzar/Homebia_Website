from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField

from . import models


class AdminPanelUserCreateForm(UserCreationForm):
	class Meta:
		model = models.CustomUserModel
		fields = ('phone_number',)

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user


class AdminPanelUserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = models.CustomUserModel
		fields = ('phone_number', 'otp_code', 'is_verified', 'is_active', 'is_staff', 'is_superuser')

	def clean_password(self):
		return self.initial["password"]


class RegistrationForm(forms.ModelForm):
	class Meta:
		model = models.CustomUserModel
		fields = ['phone_number']


class AuthenticationForm(forms.ModelForm):
	class Meta:
		model = models.Profile
		fields = ['user', 'f_name', 'l_name', 'sex', 'national_code', 'email', 'country', 'province', 'city', 'address',
				  'postal_code', 'national_card', 'auth_picture']
		widgets = {
			'address': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
		}


class InfoEditForm(forms.ModelForm):
	class Meta:
		model = models.Profile
		fields = ['email', 'country', 'province', 'city', 'address', 'postal_code']


