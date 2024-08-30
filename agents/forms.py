from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField

from . import models

class AgentAdminPanelUserCreateForm(UserCreationForm):
	class Meta:
		model = models.AgentCustomUserModel
		fields = ('phone_number',)

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user


class AgentAdminPanelUserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = models.AgentCustomUserModel
		fields = ('phone_number', 'otp_code', 'complete_info', 'is_active', 'is_staff', 'is_superuser')

	def clean_password(self):
		return self.initial["password"]


class AgentRegistrationForm(forms.ModelForm):
	class Meta:
		model = models.AgentCustomUserModel
		fields = ['phone_number']


class AgentInfoCompletionForm(forms.ModelForm):
	class Meta:
		model = models.AgentProfile
		fields = ['agent', 'f_name', 'l_name', 'sex', 'national_code', 'email', 'fixed_phone_number', 'province', 'city',
				  'postal_code', 'address', 'national_card', 'auth_picture', 'bank_card', 'bank_sheba', 'experience',
				  'course_tendency', 'introduction_way']
		widgets = {
			'address': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
		}


class AgentInfoEditForm(forms.ModelForm):
	class Meta:
		model = models.AgentProfile
		fields = ['email', 'fixed_phone_number', 'province', 'city', 'address', 'postal_code', 'bank_card', 'bank_sheba']


