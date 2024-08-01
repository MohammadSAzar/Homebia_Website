from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


from .managers import CustomUserManager


class Profile(models.Model):
	SEX_CHOICES = [
		('m', _('Male')),
		('f', _('Female')),
	]
	f_name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=_('First Name'))
	l_name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=_('Last Name'))
	sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True, verbose_name=_('Sex'))
	national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('National Code'))
	national_card = models.ImageField(upload_to='profile/national_card/', blank=True, null=True, verbose_name=_('National Card Image'))
	bank_card = models.ImageField(upload_to='profile/bank_card/', blank=True, null=True, verbose_name=_('Bank Card Image'))
	auth_picture = models.ImageField(upload_to='profile/auth_picture/', blank=True, null=True, verbose_name=_('Authentication Image'))
	country = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Country'))
	province = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Province'))
	city = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('City'))
	postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Postal Code'))
	address = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_('Address'))


class CustomUserModel(AbstractUser):
	IS_VERIFIED_CHOICES = [
		('a', _('Authenticated')),
		('n', _('Not Authenticated')),
		('i', _('In Progress')),
	]
	username = None
	# password = models.CharField(max_length=128, blank=True, null=True)
	phone_number = models.CharField(max_length=11, unique=True)
	otp_code = models.PositiveIntegerField(blank=True, null=True)
	otp_code_datetime_created = models.DateTimeField(auto_now=True)
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='user', blank=True, null=True)
	is_verified = models.CharField(max_length=10, choices=IS_VERIFIED_CHOICES, blank=True, null=True, default='n', verbose_name=_('Authentication Status'))

	objects = CustomUserManager()
	backend = 'accounts.backends.CustomAuthBackend'
	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = []



