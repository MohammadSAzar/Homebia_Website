from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


from .managers import CustomUserManager


class Profile(models.Model):
	SEX_CHOICES = [
		('m', _('Male')),
		('f', _('Female')),
	]
	APPROVAL_STATUS_CHOICES = [
		('a', _('Approved')),
		('r', _('Rejected')),
		('w', _('Waiting')),
	]
	sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)
	birthday = models.DateField(auto_now_add=False, blank=True, null=True)
	national_code = models.CharField(max_length=10, blank=True, null=True)
	national_card = models.ImageField(upload_to='profile/national_card/', blank=True, null=True)
	bank_card = models.ImageField(upload_to='profile/bank_card/', blank=True, null=True)
	auth_picture = models.ImageField(upload_to='profile/auth_picture/', blank=True, null=True)
	country = models.CharField(max_length=150, blank=True, null=True)
	province = models.CharField(max_length=150, blank=True, null=True)
	city = models.CharField(max_length=150, blank=True, null=True)
	postal_code = models.CharField(max_length=10, blank=True, null=True)
	address = models.CharField(max_length=1000, blank=True, null=True)
	status = models.CharField(max_length=10, choices=APPROVAL_STATUS_CHOICES, blank=True, null=True)


class CustomUserModel(AbstractUser):
	username = None
	phone_number = models.CharField(max_length=11, unique=True)
	otp_code = models.PositiveIntegerField(blank=True, null=True)
	otp_code_datetime_created = models.DateTimeField(auto_now=True)
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='user', blank=True, null=True)
	is_verified = models.BooleanField(default=False)

	objects = CustomUserManager()
	backend = 'accounts.backends.CustomAuthBackend'
	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = []



