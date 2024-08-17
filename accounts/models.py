from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .managers import CustomUserManager


class CustomUserModel(AbstractUser):
	IS_VERIFIED_CHOICES = [
		('a', _('Authenticated')),
		('n', _('Not Authenticated')),
		('i', _('In Progress')),
	]
	username = None
	phone_number = models.CharField(max_length=11, unique=True)
	otp_code = models.PositiveIntegerField(blank=True, null=True)
	otp_code_datetime_created = models.DateTimeField(auto_now=True)
	is_verified = models.CharField(max_length=10, choices=IS_VERIFIED_CHOICES, blank=True, null=True, default='n', verbose_name=_('Authentication Status'))

	objects = CustomUserManager()
	backend = 'accounts.backends.CustomAuthBackend'
	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = []


class Profile(models.Model):
	SEX_CHOICES = [
		('m', _('Male')),
		('f', _('Female')),
	]
	f_name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=_('First Name'))
	l_name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=_('Last Name'))
	sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True, verbose_name=_('Sex'))
	national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('National Code'))
	email = models.CharField(max_length=300, blank=True, null=True, verbose_name=_('Email'))
	national_card = models.ImageField(upload_to='profile/national_card/', blank=True, null=True, verbose_name=_('National Card Image'))
	bank_card = models.ImageField(upload_to='profile/bank_card/', blank=True, null=True, verbose_name=_('Bank Card Image'))
	auth_picture = models.ImageField(upload_to='profile/auth_picture/', blank=True, null=True, verbose_name=_('Authentication Image'))
	country = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Country'))
	province = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Province'))
	city = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('City'))
	postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Postal Code'))
	address = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_('Address'))
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)

