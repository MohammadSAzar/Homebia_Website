from django import forms

from . import models


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


# class AgentInfoEditForm(forms.ModelForm):
# 	class Meta:
# 		model = models.AgentProfile
# 		fields = ['email', 'country', 'province', 'city', 'address', 'postal_code']


